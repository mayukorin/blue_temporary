from app1.models.type import Type
from app1.models.by import By
from django.core.exceptions import ObjectDoesNotExist
from app1.widgets import SuggestWidget
from django.urls import reverse_lazy
from django import forms
'''
class ByCommentRegisterForm(forms.ModelForm):
    
    class Meta:
        model = By
        
        fields = ('conmment',)
        
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].required = False
        
'''