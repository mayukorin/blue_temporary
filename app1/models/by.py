from django.db import models
from .evaluation_tag import EvaluationTag
from .siteUser import SiteUser
from .problem import Problem


class By(models.Model):
    
    evaluation_tag = models.ForeignKey(EvaluationTag, on_delete=models.CASCADE, related_name='by_for_evalution')
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='by_for_site_user')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='by_for_problem')
    good_flag = models.BooleanField(null=True)
    