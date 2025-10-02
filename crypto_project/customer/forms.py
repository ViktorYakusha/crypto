from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Customer, Bet

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('user',)


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('quotation', 'type', 'summa')


# forms.py
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите старый пароль'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите новый пароль'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите подтверждение пароля'})