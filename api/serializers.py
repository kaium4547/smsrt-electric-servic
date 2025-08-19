from rest_framework import serializers
from apps.products.models import Product, Category
from apps.services.models import Service, ServiceCategory, ServiceSubcategory
from apps.location.models import Division, District, Upazila, Union, Village
from orders.models import Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'available', 'image', 'created', 'updated', 'category', 'category_id']


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class ServiceSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSubcategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all(), source='category', write_only=True, required=False)
    subcategory = ServiceSubcategorySerializer(read_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=ServiceSubcategory.objects.all(), source='subcategory', write_only=True, required=False)

    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'short_description', 'long_description', 'icon_class', 'image', 'price_from', 'available', 'created', 'updated', 'category', 'subcategory', 'category_id', 'subcategory_id']


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class UpazilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upazila
        fields = '__all__'


class UnionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Union
        fields = '__all__'


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone', 'address', 'division', 'district', 'upazila', 'union', 'village', 'created', 'updated', 'paid', 'status', 'items']

