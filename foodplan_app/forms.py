from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''},),
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': ''}),
    )
    password_confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': ''}),
    )
    mail = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ClientForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['name'].widget.attrs.update({'placeholder': user.username})
            self.fields['mail'].widget.attrs.update({'placeholder': user.email})

    # # TODO add validators

    class Meta:
        model = Client
        fields = ['name', 'password', 'mail']