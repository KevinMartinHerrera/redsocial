from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'faculty']
