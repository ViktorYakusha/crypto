from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django_countries.widgets import CountrySelectWidget
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField
from authtools.models import User
from .models import Customer, Bet

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('user',)


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('quotation', 'type', 'summa')

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


class UpdateUserForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ['name', 'email']


class CustomerUpdateForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите город'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес'}))
    birth_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Выберите дату рождения'}))
    job_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вид занятости'}))
    job_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес'}))
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите индекс'}),
        validators=[
            RegexValidator(
                regex=r'^[0-9]{5}(?:-[0-9]{4})?$',
                message="Почтовый индекс введен корректно"
            )
        ]
    )

    class Meta:
        model = Customer
        fields = ['phone_number', 'country', 'city', 'zip_code', 'address', 'birth_date', 'job_type', 'job_address']
        widgets = {'country': CountrySelectWidget(attrs={'class': 'form-control', 'placeholder': 'Выберите страну'})}