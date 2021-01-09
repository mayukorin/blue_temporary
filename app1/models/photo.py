from django.db import models
from .siteUser import SiteUser
from .answer import Answer
from django.utils import timezone


class Photo(models.Model):
    
    image = models.ImageField(upload_to='images', blank=True, null=True)
    upload_by = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='photo')
   
    