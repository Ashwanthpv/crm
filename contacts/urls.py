from django.urls import path, include
from rest_framework import routers
from .views import CustomerViewSet, InteractionViewSet, TaskViewSet, DealViewSet, ProductViewSet, download_data

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'interactions', InteractionViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'deals', DealViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('download-data/', download_data, name='download_data'),
]
