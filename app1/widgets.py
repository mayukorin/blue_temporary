from django import forms

class SuggestWidget(forms.TextInput):
    template_name = 'widgets/suggest.html'
    
    class Media:
        js = ['js/suggest.js']
        css = {
            'all': ['css/suggest.css']
        }
        
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' suggest form-control'
            
        else:
            self.attrs['class'] = 'suggest form-control'
    
    


