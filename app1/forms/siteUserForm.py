# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 22:13:00 2020

@author: Mayuko
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist
from app1.models.siteUser import SiteUser


class SiteUserRegisterForm(forms.ModelForm):
    
    class Meta:
        model = SiteUser
        
        fields = ('username', 'password')
        
    
        widgets = {
            'password':forms.PasswordInput(attrs={'placeholder':'パスワード'}),
            'username':forms.TextInput(attrs={'placeholder':'名前'}),
        }
      
    flag = forms.BooleanField(required=False)
    flag.widget.attrs.update({'class':'form-check-input'})
    
    
    #def clean(self):
        #super().clean()
    
   
        
        
        
    
        
        