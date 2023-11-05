from django import forms
from .models import SocialPost,SocialComments

class Socialpostforms(forms.ModelForm):  
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), max_length=280, required=True)
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'custom-file-input',
        'multiple': True,
    }), required=False)

    class Meta:
        model = SocialPost
        fields = ['body']
        
        
class SocialCommentsForm(forms.ModelForm):  
    comment= forms.CharField(widget=forms.Textarea
                              (attrs={'rows': 3}), max_length=280, required=True)
    class Meta:
        model = SocialComments
        fields = ['comment']


