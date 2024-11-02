# models.py
from django.db import models

class URLTracker(models.Model):
    url = models.URLField(unique=True)
    last_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendiente'),
            ('completed', 'Completado'),
            ('failed', 'Fallido'),
        ],
        default='pending'
    )
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.last_status}"