from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import inventory.views

router = routers.DefaultRouter()

# Inventory API endpoints
router.register(r'spareparts', views.SparePartViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]