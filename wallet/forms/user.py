from django import forms
from django.contrib.auth.forms import UserCreationForm

from wallet.models import WalletUser


class WalletUserSignupForm(UserCreationForm):
    national_id = forms.CharField(max_length=11, required=True, help_text='Enter your national ID.')

    class Meta:
        model = WalletUser
        fields = ('username', 'email', 'national_id', 'password1', 'password2')
