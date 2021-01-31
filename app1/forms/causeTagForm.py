# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:18:41 2021

@author: Mayuko
"""


from django import forms
from app1.models.cause_tag import CauseTag
from app1.models.type import Type
from app1.models.by import By
from django.core.exceptions import ObjectDoesNotExist
from app1.widgets import SuggestWidget
from django.urls import reverse_lazy

class causeTagRegisterForm(forms.ModelForm):
    
    class Meta:
        model = CauseTag
        fields = ('content','cause_type')
        
        labels = {'content': '原因タグの内容',
                  'cause_type': '原因タグのタイプ',
                  }
        
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            
            'evaluation_type': forms.Select(attrs={'class': 'form-control'})
            }
        
    cause_type = forms.ModelChoiceField(queryset=Type.objects.all().order_by('id'),
                                         empty_label=None,
                                         label='原因タグのタイプ',
                                         widget=forms.Select(attrs={'class': 'form-control'}),
                                         )
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['content'].required = False
        
    def cause_tag_exist(self):
        
        content = self.cleaned_data.get('content')
        cause_type = self.cleaned_data.get('cause_type')
        
        try:
            cause_tag = CauseTag.objects.get(content=content, cause_type__id=cause_type.id)
            
        except ObjectDoesNotExist:
            
            print('評価タグ自体がまだ存在しないか、フォームの入力を間違えている')
            
            return None
        
        return cause_tag
        
        

    
CauseTagRegisterFormSet = forms.modelformset_factory(model=CauseTag, form=causeTagRegisterForm, extra=1, can_delete=False)

'''
class PreviousCauseTagRegisterForm(forms.ModelForm):
    
    class Meta:
        model = CauseTag
        fields = ('content','cause_type')
        
        labels = {'content': '原因タグの内容',
                  'cause_type': '原因タグのタイプ',
                  }
        
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            
            'evaluation_type': forms.Select(attrs={'class': 'form-control'})
            }
        
    cause_type = forms.ModelChoiceField(queryset=Type.objects.all().order_by('id'),
                                         empty_label=None,
                                         label='原因タグのタイプ',
                                         widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
                                         )
    
    overcome_flag = forms.BooleanField()
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        if self.errors:
            print(self.errors)
    
previousCauseTagRegisterFormSet = forms.modelformset_factory(model=CauseTag, form=PreviousCauseTagRegisterForm, extra=0, can_delete=False)
'''

class  WithForPreviousCauseTagRegisterForm(forms.Form):
    overcome_flag = forms.BooleanField()
    
WithForPreviousCauseTagRegisterFormSet = forms.formset_factory(form=WithForPreviousCauseTagRegisterForm)