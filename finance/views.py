from django.shortcuts import render
from django.views.decorators.http import *
from datetime import datetime
from .models import *
from .forms import *

# MAIN PAGE
@require_http_methods(["GET", "POST"])
def render_main_page(request):
    save_account(request)
    context = get_accounts()
    context['form'] = AccountForm
    return render(request, 'finance/main.html', context)

def get_accounts():
    accounts = [item for item in Account.objects.all()]
    return {"accounts": accounts, "number": len(accounts)}

def save_account(request):
    form = AccountForm(request.POST)

    if form.is_valid():
        for i in form.fields:
            if i is None: break
        else: form.save()

    return render_main_page

# ACCOUNT PAGE
@require_http_methods(["GET", "POST"])
def render_account_page(request, name):
    if request.POST:
        save_charge(request, name)
    context = get_charges(name)
    account = Account.objects.get(pk=name)
    context['account_info'] = (account.name, account.last_name, account.email)
    return render(request, 'finance/account.html', context)


def get_charges(name):
    # charges = [item for item in Charge.objects.all().filter(self.account.name==name)]
    charges = []
    total = 0.0
    for i in Charge.objects.all():
        if i.account.name == name:
            charges.append(i)
            total += i.value
    return {"charges": charges, "number": len(charges), "total": total, "name": name}

def save_charge(request, name):
    value = request.POST['value']
    try:
        value = float(value)
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        account = Account.objects.get(pk=name)
        tmp_charge = Charge(value=value, date=date, account=account)
        tmp_charge.save()
    except: pass
    finally:
        return render_account_page
