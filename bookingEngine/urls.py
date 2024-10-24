from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookingSettingsViewSet, ResourceTypeViewSet,
    AgentViewSet, ResourceViewSet, BookingViewSet,
    BlockedTimeViewSet
)

router = DefaultRouter()
router.register(r'settings', BookingSettingsViewSet)
router.register(r'resource-types', ResourceTypeViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'blocked-times', BlockedTimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]