from app1.models.type import Type
from app1.models.by_comment import ByComment
from django.core.exceptions import ObjectDoesNotExist
from app1.widgets import SuggestWidget
from django.urls import reverse_lazy
from django import forms

class ByCommentUpdateForm(forms.ModelForm):
    
    class Meta:
        model = ByComment
        
        fields = {'content',}
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            }
        
        labels = {
            'content': 'コメント',
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False
        
    def clean_content(self):
        
        content = self.cleaned_data['content']
        
        if len(content) == 0:
            raise forms.ValidationError('コメントを入力してください')
            
        return content

