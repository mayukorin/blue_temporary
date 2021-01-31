from django.db import models
from .problem import Problem
from .cause_tag import CauseTag
from .siteUser import SiteUser
from .with_model import With

class LatestWith(models.Model):
    
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    cause_tag = models.ForeignKey(CauseTag, related_name="latest_withes", on_delete=models.CASCADE)
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    latest_with = models.OneToOneField(With, on_delete=models.PROTECT, null=True)
    

