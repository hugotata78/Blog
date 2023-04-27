from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(UserCreationForm):

    username = forms.CharField(help_text=None)
    email = forms.EmailField(help_text=None)
    first_name = forms.CharField(help_text=None, label='Nombre')
    last_name = forms.CharField(help_text=None, label='Apellido')
    password1 = forms.CharField(help_text=None, label='Password')
    password2 = forms.CharField(help_text=None, label='Confirmar Password')
    
    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email", "password1", "password2")

class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(help_text=None)
    email = forms.EmailField(help_text=None)
    first_name = forms.CharField(help_text=None, label='Nombre')
    last_name = forms.CharField(help_text=None, label='Apellido')
    
    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email")