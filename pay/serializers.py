from rest_framework import serializers
from .models import URLTracker

class URLTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLTracker
        fields = ['id', 'url', 'last_status', 'last_checked', 'created_at']
        read_only_fields = ['last_checked', 'created_at']