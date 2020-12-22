# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:50:53 2020

@author: Mayuko
"""


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'app1'

urlpatterns = [
    
    path('',views.chapter_view.chapter_list,name='chapter_list'),
    path('siteUser/register',views.siteUser_view.siteUser_register,name='siteUser_register'),
    
]