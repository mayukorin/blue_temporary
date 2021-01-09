# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:28:25 2021

@author: Mayuko
"""


from django import forms
from app1.models.answer import Answer


class AnswerRegisterForm(forms.ModelForm):
    
    class Meta:
        
        model = Answer
        fields = ('solve_plan_date', 'solve_date', 'actual_time', 'correct_situation')
        
        widgets = {
            'solve_plan_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'solve_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
            }
        
        input_formats = {
            'solve_plan_date': ['%Y-%m%dT%H:%M'],
            'solve_date': ['%Y-%m%dT%H:%M'],
            }
        
        labels = {
            'actual_time': '解答時間/分', 
            'solve_date': '解いた日付',
            'solve_plan_date': '解答予定日',
            'correct_situation': '解答状況',
            }
        
    photo = forms.ImageField(
        label='解答写真',
         )
    
    comment = forms.CharField(
        label='コメント', 
        widget=forms.Textarea()
        )
    
    def clean_solve_plan_date(self):
        
        solve_plan_date = self.cleaned_data['solve_plan_date']
        
        if solve_plan_date is None:
            
            raise forms.ValidationError("解答予定日を入力してください")
        
        return self.cleaned_data['solve_plan_date']
    
    def clean_photo(self):
        
        photo = self.cleaned_data['photo']
        print(photo)
        
        return photo
    
    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            
        self.fields['correct_situation'].widget.attrs.update({'class': 'form-control'})
        

class AnswerUpdateForm(forms.ModelForm):
    
    class Meta:
        
        model = Answer
        fields = ('solve_plan_date', 'solve_date', 'actual_time', 'correct_situation')
        
        widgets = {
            'solve_plan_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'solve_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
            }
        
        input_formats = {
            'solve_plan_date': ['%Y-%m%dT%H:%M'],
            'solve_date': ['%Y-%m%dT%H:%M'],
            }
        
        labels = {
            'actual_time': '解答時間/分', 
            'solve_date': '解いた日付',
            'solve_plan_date': '解答予定日',
            'correct_situation': '解答状況'
            }
    
    def clean_solve_plan_date(self):
        
        solve_plan_date = self.cleaned_data['solve_plan_date']
        
        if solve_plan_date is None:
            
            raise forms.ValidationError("解答予定日を入力してください")
        
        return self.cleaned_data['solve_plan_date']

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            
        self.fields['correct_situation'].widget.attrs.update({'class': 'form-control'})
