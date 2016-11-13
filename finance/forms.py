from django.forms import ModelForm
from .models import Account, Charge

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'last_name', 'email']


class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = ['value']
