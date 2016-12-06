from django.views.decorators.http import *
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error
from django.db import transaction
from .models import *
from .forms import *

#
# Main page
# Render main page with log in forms
#
@require_http_methods(["GET", "POST"])
def render_main_page(request):
    log_in(request)
    context = {}
    return render(request, 'finance/main.html', context)

def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not (username and password):
        return render(request, 'finance/main.html')
    user = authenticate(username=username, password=password)
    if not user:
        error('Wrong login or password!')
        return render(request, 'login.html')
    login(request, user)
    return render_user_page(request, user.name)

#
# Sign Up page
# Render sign up page with sign up forms
#
@require_http_methods(["GET", "POST"])
def render_sign_up_page(request):
    sign_up(request)
    context = {}
    return render(request, 'finance/sign_up.html', context)

@transaction.atomic(savepoint=False)
def sign_up(request):
    form = UserForm(request.POST)
    form.save_if_valid()
    return render_main_page

#
# User page
# Render user page with list of users's accounts
# and form for adding accounts
#
@require_http_methods(["GET", "POST"])
def render_user_page(request, name):
    user = User.objects.get(name=name)
    save_account(request, user)
    context = get_user_and_accounts(user)
    return render(request, 'finance/user.html', context)

def get_user_and_accounts(user):
    accounts = []
    number = 0
    charges = list(Charge.objects.all())
    for acc in Account.objects.all():
        if acc.user.name == user.name:
            total = 0
            for charge in charges:
                if charge.account == acc:
                    total += charge.value
            accounts.append([acc, total])
            number += 1
    return {'user': user, 'accounts': accounts, 'number': number}

@require_http_methods(["POST"])
def save_account(request, user):
    if 'add-account' in request.POST:
        account_QS = list(Account.objects.all())
        if len(account_QS) != 0:
            name = int(account_QS[-1].name, 16) + 1
            name = str(hex(name)).upper()
        else:
            name = '0X64'
        a = Account(name=name, user=user)
        a.save()

#
# Account page
# Render account page with list of account's charges
# and form for adding charges
#
@require_http_methods(["GET", "POST"])
def render_account_page(request, name, account_name):
    user = User.objects.get(pk=name)
    account = Account.objects.get(pk=account_name)
    save_charge(request, account)
    context = get_charges(account)
    context['user'] = user
    return render(request, 'finance/account.html', context)

def get_charges(account):
    charges, total = [], 0.0
    for i in Charge.objects.all():
        if i.account.name == account.name:
            charges.append(i)
            total += i.value
    return {"charges": charges, "number": len(charges), "total": total, 'account': account}

@require_http_methods(["POST"])
@transaction.atomic(savepoint=False)
def save_charge(request, account):
    form = ChargeForm(request.POST)
    form.save_if_valid(account)
    return render_account_page

#
# Users page
# Render page with list of users
#
@require_http_methods(["GET", "POST"])
def render_users_page(request):
    context = get_users()
    return render(request, 'finance/users.html', context)

def get_users():
    users = [item for item in User.objects.all()]
    return {"users": users, "number": len(users)}
