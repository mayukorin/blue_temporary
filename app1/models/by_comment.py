from django.db import models
from .by import By
from django.utils import timezone

class ByComment(models.Model):
    
    content = models.TextField(blank=True, null=True)
    by = models.ForeignKey(By, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
