from rest_framework import viewsets, permissions
from apps.products.models import Product, Category
from apps.services.models import Service, ServiceCategory, ServiceSubcategory
from apps.location.models import Division, District, Upazila, Union, Village
from orders.models import Order
from .serializers import (
    ProductSerializer, CategorySerializer,
    ServiceSerializer, ServiceCategorySerializer, ServiceSubcategorySerializer,
    DivisionSerializer, DistrictSerializer, UpazilaSerializer, UnionSerializer, VillageSerializer,
    OrderSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceSubcategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceSubcategory.objects.all()
    serializer_class = ServiceSubcategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DivisionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class UpazilaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Upazila.objects.all()
    serializer_class = UpazilaSerializer


class UnionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Union.objects.all()
    serializer_class = UnionSerializer


class VillageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('user')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

