from django.urls import path
from . import views

urlpatterns = [
    path('api/track-url/', views.track_url, name='track-url'),
    path('api/check-url-status/', views.check_url_status, name='check-url-status'),
    path('api/trackers/', views.URLTrackerListView.as_view(), name='tracker-list'),
    path('api/trackers/<int:pk>/', views.URLTrackerDetailView.as_view(), name='tracker-detail'),
]