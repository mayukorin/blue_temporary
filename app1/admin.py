from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app1.models.siteUser import SiteUser
from app1.models.subject import Subject
from app1.models.chapter import Chapter
from app1.models.section import Section
from app1.models.problem_group import Problem_group
from app1.models.problem import Problem
from app1.models.similar import Similar
from app1.models.develop import Develop
from app1.models.photo import Photo
from app1.models.answer import Answer
from app1.models.correct_situation import CorrectSituation
from app1.models.type import Type
from app1.models.evaluation_tag import EvaluationTag
from app1.models.by import By
from app1.models.cause_tag import CauseTag
from app1.models.with_model import With
from app1.models.latest_with import LatestWith
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = SiteUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('flag',)}),)
    list_display = ['username', 'email', 'flag']
 
 
admin.site.register(SiteUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Problem_group)
admin.site.register(Problem)
admin.site.register(Similar)
admin.site.register(Develop)
admin.site.register(Photo)
admin.site.register(Answer)
admin.site.register(CorrectSituation)
admin.site.register(Type)
admin.site.register(EvaluationTag)
admin.site.register(By)
admin.site.register(CauseTag)
admin.site.register(With)
admin.site.register(LatestWith)
# Register your models here.
