from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm




class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Никнейм'
