from channels.generic.websocket import AsyncJsonWebsocketConsumer
from users.models import TechnicianTracking, SupportChatMessage
from django.contrib.auth.models import AnonymousUser

class TechnicianLocationConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'tech_locations'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # Expected: {"type": "update", "lat": 23.7, "lng": 90.4}
        typ = content.get('type')
        if typ == 'update':
            lat = content.get('lat')
            lng = content.get('lng')
            user = self.scope.get('user')
            if not user or isinstance(user, AnonymousUser) or getattr(user, 'user_type', None) != 'technician':
                return
            # Persist last known location if tracking enabled
            try:
                tracking, _ = TechnicianTracking.objects.get_or_create(technician_id=user.id)
                if tracking.enabled:
                    tracking.current_latitude = lat
                    tracking.current_longitude = lng
                    tracking.save(update_fields=['current_latitude', 'current_longitude', 'updated_at'])
            except Exception:
                pass
            await self.channel_layer.group_send(self.group_name, {
                'type': 'broadcast_location',
                'payload': {
                    'username': getattr(user, 'username', 'unknown'),
                    'lat': lat,
                    'lng': lng,
                }
            })

    async def broadcast_location(self, event):
        await self.send_json(event['payload'])

class SupportChatConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'support_chat'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # expects: {type:'message', name, email, category, message, lat?, lng?}
        if content.get('type') == 'message':
            user = self.scope.get('user')
            name = content.get('name') or (getattr(user, 'get_full_name', lambda: None)() or getattr(user, 'username', None))
            email = content.get('email')
            category = content.get('category') or 'other'
            msg = content.get('message')
            lat = content.get('lat')
            lng = content.get('lng')
            try:
                SupportChatMessage.objects.create(
                    user=user if user and not isinstance(user, AnonymousUser) else None,
                    name=name,
                    email=email,
                    category=category,
                    message=msg,
                    latitude=lat if lat is not None else None,
                    longitude=lng if lng is not None else None,
                )
            except Exception:
                pass
            await self.channel_layer.group_send(self.group_name, {
                'type': 'broadcast_chat',
                'payload': {
                    'name': name or 'Guest',
                    'email': email,
                    'category': category,
                    'message': msg,
                }
            })

    async def broadcast_chat(self, event):
        await self.send_json(event['payload'])