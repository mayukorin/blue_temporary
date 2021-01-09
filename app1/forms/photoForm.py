# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 18:09:39 2021

@author: Mayuko
"""


from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist
from app1.models.siteUser import SiteUser
from app1.models.photo import Photo


class PhotoRegisterForm(forms.ModelForm):
    
    class Meta:
        
        model = Photo
        fields = ('image',)
        
    comment = forms.CharField(
        label='コメント', 
        widget=forms.Textarea(),
        required=False,
        )
        
    def clean_image(self):
        
        image = self.cleaned_data['image']
        
        if image is None:
            
            raise forms.ValidationError("解答写真を登録してください")
            
        return image