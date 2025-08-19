from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet,
    ServiceCategoryViewSet, ServiceSubcategoryViewSet, ServiceViewSet,
    DivisionViewSet, DistrictViewSet, UpazilaViewSet, UnionViewSet, VillageViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'service-subcategories', ServiceSubcategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'divisions', DivisionViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'upazilas', UpazilaViewSet)
router.register(r'unions', UnionViewSet)
router.register(r'villages', VillageViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

