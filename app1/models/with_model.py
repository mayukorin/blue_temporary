from django.db import models
from .answer import Answer
from .cause_tag import CauseTag
from .siteUser import SiteUser


class With(models.Model):
    
    answer = models.ForeignKey(Answer, related_name="withes", on_delete=models.CASCADE)
    cause_tag = models.ForeignKey(CauseTag, related_name="withes", on_delete=models.CASCADE)
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    latest_with = models.ForeignKey('LatestWith', on_delete=models.CASCADE, null=True)
    overcome_flag = models.BooleanField(null=True)
