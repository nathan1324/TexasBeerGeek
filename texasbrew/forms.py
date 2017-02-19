from django import forms
from django.contrib.auth.models import User

from .models import Brewery, Beer


class BrewForm(forms.ModelForm):

    class Meta:
        model = Brewery
        fields = ['brew_name', 'brew_location', 'brew_logo']


class BeerForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = ['beer_name', 'beer_type', 'beer_image']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
