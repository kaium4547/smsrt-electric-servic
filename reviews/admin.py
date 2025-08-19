from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "content_type", "object_id", "rating", "status", "created"]
    list_filter = ["status", "rating", "created", "content_type"]
    search_fields = ["comment", "user__username"]

