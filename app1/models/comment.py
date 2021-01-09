from django.db import models
from django.utils import timezone
from .siteUser import SiteUser
from .answer import Answer
from .photo import Photo


class Comment(models.Model):
    
    comment = models.TextField(blank=True, null=True)
    by = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    photo = models.ForeignKey(Photo, on_delete=models.PROTECT, null=True, related_name='reply_comment')
    origin_photo = models.OneToOneField(Photo, on_delete=models.PROTECT, null=True, related_name='origin_comment')

