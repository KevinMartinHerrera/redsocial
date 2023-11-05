from django import forms
from .models import Profile, FriendRequest, User

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = []

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto_de_perfil', 'red_social', 'ciudad', 'birthdate', 'bio']

    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}))

    # Agrega un campo para mostrar la foto de perfil actual
    foto_de_perfil_actual = forms.ImageField(
        required=False,  # No es necesario proporcionar una imagen
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),  # Aplica clases CSS si es necesario
    )

    def __init__(self, *args, **kwargs):
        # Obtén el perfil actual desde el contexto
        profile = kwargs.pop('profile', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        # Llena los campos del formulario con los valores del perfil actual
        if profile:
            self.fields['foto_de_perfil'].initial = profile.foto_de_perfil
            self.fields['red_social'].initial = profile.red_social
            self.fields['ciudad'].initial = profile.ciudad
            self.fields['birthdate'].initial = profile.birthdate
            self.fields['bio'].initial = profile.bio

from allauth.account.forms import SignupForm
from allauth.account.forms import BaseSignupForm
from .models import Profile
from django import forms
from social.models import Facultad

class CustomSignupForm(SignupForm, BaseSignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    facultad = forms.ModelChoiceField(queryset=Facultad.objects.all(), label="Facultad", required=False)
