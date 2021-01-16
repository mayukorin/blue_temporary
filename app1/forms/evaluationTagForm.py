# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:22:52 2021

@author: Mayuko
"""


from django import forms
from app1.models.evaluation_tag import EvaluationTag
from app1.models.type import Type
from app1.models.by import By
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
            
            'evaluation_type': forms.Select(attrs={'class': 'form-control'})
            }
        
        
        
        
    evaluation_type = forms.ModelChoiceField(queryset=Type.objects.all().order_by('id'),
                                             empty_label=None,
                                             label='主に身につくこと',
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(label='コメント（任意）',
                              required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    
    
    def __init__(self, user_id, problem_id, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.user_id = user_id
        self.problem_id = problem_id
        self.evaluation_tag_cache = None
        a = SuggestWidget()
        
        self.fields['content'].required = False
        
        if self.errors and 'content' in self.errors:
            
            self.fields['content'].widget.attrs.update({'class': 'form-control is-invalid suggest'})
            
            
    def clean_content(self):
        
        content = self.cleaned_data['content']
        if content is None:
            
            raise forms.ValidationError('評価タグの内容を入力してください')
            
        return content
    
    def clean(self):
        
        content = self.cleaned_data.get('content')
        evaluation_type = self.cleaned_data.get('evaluation_type')
        
        try:
            evaluation_tag = EvaluationTag.objects.get(content=content, evaluation_type__id=evaluation_type.id)
            
        except ObjectDoesNotExist:
            
            print('評価タグ自体がまだ存在しないか、フォームの入力を間違えている')
            
            return
        
        self.evaluation_tag_cache = evaluation_tag
        
        try:
            by = By.objects.get(evaluation_tag__id=self.evaluation_tag_cache.id, site_user__id=self.user_id, problem__id=self.problem_id)
            
        except ObjectDoesNotExist:
            
            print('まだその評価タグをその問題に自分では登録していない')
            
            return
        
        raise forms.ValidationError('その問題に対するその評価タグは以前に登録しています')
            
    
    def evaluation_tag_exist(self):
        
        
        return self.evaluation_tag_cache
        