from django.forms import ModelForm
from .models import *
from datetime import datetime

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password', 'phone', 'address']
    def save_if_valid(self):
        if self.is_valid():
            for i in self.fields:
                if i is None: break
            else: self.save()

class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = ['value']
    def save_if_valid(self, account):
        if self.is_valid():
            try:
                value = self.cleaned_data['value']
                date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                tmp = Charge(value=value, date=date, account=account)
                tmp.save()
            except:
                pass
