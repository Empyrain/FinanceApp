from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'phone', 'address']

    def save_if_valid(self):
        if self.is_valid():
            try:
                int(self.cleaned_data['phone'])
            except:
                return False
            print('a')
            return True
        else:
            print('b')
            return False

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save_if_valid(self):
        print(1)
        print(self._errors)
        print(self.cleaned_data['username'])
        print(self.cleaned_data['email'])
        print(self.cleaned_data['password'])
        if self.is_valid():
            print(self.username, self.email, self.password)
            print(1)
            if User.objects.all(username=username) is not None:
                print(2)
                return True
            else:
                print(3)
                return False
        else:
            print(4)
            return False

class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = ['value']
    def save_if_valid(self, account):
        if self.is_valid():
            try:
                value = self.cleaned_data['value']
                value = round(value, 2)
                date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                tmp = Charge(value=value, date=date, account=account)
                tmp.save()
            except:
                pass
