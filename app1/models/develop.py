from django.db import models
from .problem import Problem


class Develop(models.Model):
    
    from_problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='easy')
    to_problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='difficult')
    