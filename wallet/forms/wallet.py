from typing import cast

from django import forms

from wallet.models import Wallet, Country, WalletUser


class WalletCreateForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance', 'country', 'name']  # Exclude user from the form fields
        widgets = {
            'balance': forms.NumberInput(attrs={'placeholder': 'Enter balance'}),
            'country': forms.Select(),
            'name': forms.TextInput(attrs={'placeholder': 'Enter wallet name'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop the user from kwargs
        super(WalletCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        wallet = super(WalletCreateForm, self).save(commit=False)
        wallet.user = WalletUser.objects.get(user_ptr_id=self.user)  # Set the user
        if commit:
            wallet.save()
        return wallet


class WalletUpdateForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance', 'country', 'name']
        widgets = {
            'balance': forms.NumberInput(attrs={'placeholder': 'Enter balance'}),
            'country': forms.Select(choices=Country.choices()),
            'name': forms.TextInput(attrs={'placeholder': 'Enter wallet name'}),
        }
