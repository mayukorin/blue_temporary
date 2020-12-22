# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 21:57:48 2020

@author: Mayuko
"""
from django.views import View
from app1.models.chapter import Chapter, Subject
from django.shortcuts import render
from django.db import connection
from django.db.models import Count
from app1.forms.siteUserForm import SiteUserRegisterForm
from django.contrib import messages

class SiteUserRegisterView(View):
    def get(self, request, *args, **kwargs):
      
        context = {
            'form':SiteUserRegisterForm(),
            }
       
        return render(request, 'siteUser/register.html', context)
    
    def post(self,request,*args, **kwargs):
        
        form = SiteUserRegisterForm(request.POST)
        
        if not form.is_valid():
            
            
            return render(request,'siteUser/register.html', {'form':form})
            
        siteUser = form.save(commit = False)
        siteUser.set_password(form.cleaned_data['password'])
        siteUser.flag = 1 if form.cleaned_data['flag'] == True else 0
        
        siteUser.save()
        
        messages.success(request, "ユーザ登録が完了しました")
            
        
        context = {
            'form':SiteUserRegisterForm(),
            }
       
        return render(request, 'siteUser/register.html', context)

siteUser_register = SiteUserRegisterView.as_view()
