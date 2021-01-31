from django import forms
from app1.models.cause_tag import CauseTag
from app1.models.type import Type
from app1.models.by import By
from app1.models.with_model import With
from app1.models.latest_with import LatestWith
from django.core.exceptions import ObjectDoesNotExist
from app1.widgets import SuggestWidget
from django.urls import reverse_lazy


class WithForPreviousCauseTagRegisterForm(forms.ModelForm):
    
    class Meta:
        model = With
        fields = ('overcome_flag',)
        
        widgets = {
            'overcome_flag': forms.CheckboxInput(),
            }
  
