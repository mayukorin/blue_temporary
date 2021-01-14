# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:22:52 2021

@author: Mayuko
"""


from django import forms
from app1.models.evaluation_tag import EvaluationTag
from app1.models.type import Type
from django.core.exceptions import ObjectDoesNotExist
from app1.widgets import SuggestWidget
from django.urls import reverse_lazy

class EvaluationTagRegisterForm(forms.ModelForm):
    
    class Meta:
        model = EvaluationTag
        
        fields = ('evaluation_type','content',)
        
        labels = {
            'content': '評価タグの内容',
            'evaluation_type': '主に身につく力'
            }
        
        widgets = {
            'content': SuggestWidget(attrs={'data-url': reverse_lazy('app1:evaluation_tag_suggest'), 'name': 'content'}),
            #'content': forms.TextInput(),
            'evaluation_type': forms.Select(attrs={'class': 'form-control'})
            }
        
        
        
        
    evaluation_type = forms.ModelChoiceField(queryset=Type.objects.all().order_by('id'),
                                             empty_label=None,
                                             label='主に身につくこと',
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    
    
    
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        a = SuggestWidget()
        print(a.media)
        
        self.fields['content'].required = False
        
        if self.errors and 'content' in self.errors:
            
            self.fields['content'].widget.attrs.update({'class': 'form-control is-invalid suggest'})
            
            
    def clean_content(self):
        
        content = self.cleaned_data['content']
        print("ooo")
        print(content)
        if content is None:
            
            raise forms.ValidationError('評価タグの内容を入力してください')
            
        return content
    
    def evaluation_tag_exist(self):
        
        content = self.cleaned_data['content']
        evaluation_type_id = self.cleaned_data['evaluation_type'].id
        
        try:
            evaluation_tag = EvaluationTag.objects.get(content=content, evaluation_type__id=evaluation_type_id )
            
        except ObjectDoesNotExist:
            
            print('新しい評価タグ')
            
            return None
        
        return evaluation_tag