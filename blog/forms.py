from .models import blog, User
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import authenticate


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']


class blogForm(forms.ModelForm):
    class Meta:
        model = blog
        fields = 'title', 'catagory', 'description'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 60, 'style': 'resize:none;'}),
        }
