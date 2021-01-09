# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 12:42:18 2021

@author: Mayuko
"""


from django import forms
from app1.models.comment import Comment


class CommentUpdateForm(forms.ModelForm):
    
    class Meta:
        
        model = Comment
        
        fields = {'comment'}
        
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'})
            }
        
        labels = {
            'comment': 'コメント'}
        
        requires = {
            'comment': False}
    
    def clean_comment(self):
        
        comment = self.cleaned_data['comment']
        
        if len(comment) == 0 or comment is None:
            
            raise forms.ValidationError('コメントを入力してください')
            
        return comment
        
    
    