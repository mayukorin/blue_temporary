from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app1.models.siteUser import SiteUser
from app1.models.subject import Subject
from app1.models.chapter import Chapter
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = SiteUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('flag',)}),)
    list_display = ['username', 'email', 'flag']
 
 
admin.site.register(SiteUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Chapter)
# Register your models here.
