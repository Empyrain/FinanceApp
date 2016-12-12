from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'phone', 'address']

    def save_if_valid(self, user):
        if self.is_valid():
            try:
                int(self.cleaned_data['phone'])
                name = self.cleaned_data['name']
                surname = self.cleaned_data['surname']
                phone = self.cleaned_data['phone']
                address = self.cleaned_data['address']
                profile = Profile(name=name, surname=surname, phone=phone, address=address, user=user)
                return True, profile
            except: return False
        else: return False


class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = ['value']
    def save_if_valid(self, account):
        if self.is_valid():
            try:
                value = self.cleaned_data['value']
                value = round(value, 2)
                tmp = Charge(value=value, account=account)
                tmp.save()
            except:
                pass
