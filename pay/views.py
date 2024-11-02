from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import URLTracker
from .serializers import URLTrackerSerializer
import requests
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def track_url(request):
    """
    Create or retrieve a URL tracker.
    """
    url = request.data.get('url')
    if not url:
        raise ValidationError({'url': 'This field is required.'})
    
    # Validate URL format
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValidationError({'url': 'Invalid URL format.'})
    except Exception as e:
        raise ValidationError({'url': 'Invalid URL format.'})
    
    tracker, created = URLTracker.objects.get_or_create(
        url=url,
        defaults={'last_status': 'pending'}
    )
    serializer = URLTrackerSerializer(tracker)
    return Response(serializer.data)

@api_view(['POST'])
def check_url_status(request):
    """
    Check the current status of a URL and update the tracker.
    """
    url = request.data.get('url')
    if not url:
        raise ValidationError({'url': 'This field is required.'})
    
    try:
        tracker = URLTracker.objects.get(url=url)
    except URLTracker.DoesNotExist:
        raise ValidationError({'url': 'URL not found in tracking system.'})
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        final_url = response.url
        
        # Define status based on URL patterns and response
        status = 'pending'
        if response.status_code >= 400:
            status = 'failed'
        elif any(keyword in final_url.lower() for keyword in ['success', 'completed', 'thank']):
            status = 'completed'
        elif any(keyword in final_url.lower() for keyword in ['failed', 'cancelled', 'error']):
            status = 'failed'
        
        tracker.last_status = status
        tracker.last_checked = timezone.now()
        tracker.save()
        
        serializer = URLTrackerSerializer(tracker)
        return Response({
            'tracker': serializer.data,
            'final_url': final_url,
            'response_code': response.status_code
        })
        
    except requests.RequestException as e:
        logger.error(f"Error checking URL {url}: {str(e)}")
        return Response({
            'error': 'Failed to check URL status',
            'detail': str(e)
        }, status=500)

class URLTrackerListView(generics.ListCreateAPIView):
    """
    List all URL trackers or create a new one.
    """
    queryset = URLTracker.objects.all().order_by('-created_at')
    serializer_class = URLTrackerSerializer
    
    def perform_create(self, serializer):
        serializer.save(last_status='pending')

class URLTrackerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a URL tracker.
    """
    queryset = URLTracker.objects.all()
    serializer_class = URLTrackerSerializer