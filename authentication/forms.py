from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserAccount(UserCreationForm):
    username = forms.CharField(label='Username', min_length=4, max_length=150, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    email = forms.EmailField(label='Email', max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8, help_text='Required. Minimum 8 characters, at least one letter and one number.')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']