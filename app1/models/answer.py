from django.db import models
from django.utils import timezone
from .siteUser import SiteUser
from .problem import Problem
from .correct_situation import CorrectSituation

class Answer(models.Model):
    
    correct_situation = models.ForeignKey(CorrectSituation, on_delete=models.CASCADE, null=True)
    solve_plan_date = models.DateTimeField(default=timezone.now, blank=True)
    solve_date = models.DateTimeField(default=timezone.now, null=True)
    actual_time = models.IntegerField(null=True)
    student = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)