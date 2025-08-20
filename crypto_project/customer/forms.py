from django import forms
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('user',)

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return cd['password2']
    # #
    # # def save(self, commit=True):
    # #     user = super().save(commit=False)
    # #     # Save custom fields to the Profile model
    # #     if commit:
    # #         user.save()
    # #         profile = Profile.objects.create(user=user,
    # #                                          phone_number=self.cleaned_data['phone_number'],
    # #                                          address=self.cleaned_data['address'])
    # #     return user