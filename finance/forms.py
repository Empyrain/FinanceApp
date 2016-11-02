from decimal import Decimal
from datetime import date

class ChargeForm(forms.Form):
    value = forms.DecimalField(label='value', required=True)
    date = forms.DateField(label='date', required=True)

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if velue < 0:
            #date юзера поступает в виде строки вида 'yyyy/mm/dd'
            date = self.cleaned_data.get('date')
            date_now = (date.today().year, date.today().month, date.today().day)
            if date_vs_date(date_now, date.split('/')):
                raise ValidationError('Must be positive')
            else:
                return {'value' : value, 'date': date}
        else:
            return {'value' : value, 'date': date}

def date_vs_date(date1, date2):
    if date1[0] < date2[0]: return False
    elif date1[0] > date2[0]: return True
    elif date1[1] < date2[1]: return False
    elif date1[1] > date2[1]: return True
    elif date1[2] => date2[2]: return True
    else: return False
