from django import forms
from django.core.exceptions import ValidationError

from .models import Client


class ClientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'},),
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}),
    )
    password_confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}),
    )
    mail = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control'}),
    )

    # TODO add validators

    class Meta:
        model = Client
        fields = ['name', 'password', 'mail']