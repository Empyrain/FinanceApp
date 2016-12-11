from django.views.decorators.http import *
from django.shortcuts import render, redirect
from django.db import transaction

from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

#
# Main page
# Render main page with log in forms
#
@require_http_methods(["GET", "POST"])
def render_main_page(request):
    if request.POST.get('username') is not None:
        login_result = log_in(request)
        return login_result
    else:
        context = {}
        return render(request, 'finance/main.html', context)

def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/users/{}'.format(username))
    else:
        context = {'errors': 'Wrong login data. Try again.'}
        return render(request, 'finance/main.html', context)


#
# Sign Up page
# Render sign up page with sign up forms
#
@require_http_methods(["GET", "POST"])
def render_sign_up_page(request):
    rendered = sign_up(request)
    if rendered is not None:
        return rendered
    context = {}
    return render(request, 'finance/sign_up.html', context)

@transaction.atomic(savepoint=False)
def sign_up(request):
    if request.POST.get('username') is not None:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        profile_form = ProfileForm(request.POST)
        if profile_form.save_if_valid() is True:
            user = User.objects.create_user(username=username, email=email, password=password)
            if user is not None:
                user.save()
                profile_form.save()
                return redirect('/')

            else:
                context = {'errors': 'Invalid data!'}
                render(request, 'finance/sign_up.html', context)
        else:
            context = {'errors': 'Invalid data!'}
            render(request, 'finance/sign_up.html', context)

#
# Logout page
#
@require_http_methods(["GET", "POST"])
def render_logout_page(request):
    auth.logout(request)
    return redirect('/')

#
# User page
# Render user page with list of users's accounts
# and form for adding accounts
#
@login_required
@require_http_methods(["GET", "POST"])
def render_user_page(request, username):
    if username == request.user.username:
        user = User.objects.get(username=username)
        save_account(request, user)
        context = get_user_and_accounts(user)
        return render(request, 'finance/user.html', context)
    else:
        raise PermissionDenied

def get_user_and_accounts(user):
    # тут так фигово, потому что в шаблоне нужен список [[account, total], [...], ...]
    accounts = list(user.accounts.all())
    account_charges = [list(account.charges.all()) for account in accounts]
    math_total = lambda account_charges: sum([i.value for i in account_charges])

    accs_and_totals = []
    total = 0
    for counter, account in enumerate(accounts):
        tmp = math_total(account_charges[counter])
        accs_and_totals.append([account, tmp])
        total += tmp
    total = round(total, 2)
    return {'user': user, 'accs_and_totals': accs_and_totals, 'number': len(accounts), 'total': total}

@require_http_methods(["POST"])
def save_account(request, user):
    if 'add-account' in request.POST:
        accounts = list(Account.objects.all())
        name = give_name(accounts)
        a = Account(name=name, user=user)
        a.save()

def give_name(accounts):
    if len(accounts) != 0:
        name = int(accounts[-1].name, 16) + 1
        name = str(hex(name)).upper()
    else:
        name = '0X64'
    return name

#
# Account page
# Render account page with list of account's charges
# and form for adding charges
#
@login_required
@require_http_methods(["GET", "POST"])
def render_account_page(request, username, account_name):
    if username == request.user.username:
        account = Account.objects.get(pk=account_name)
        save_charge(request, account)
        context = get_charges(account)
        context['user'] = User.objects.get(username=username)
        return render(request, 'finance/account.html', context)
    else:
        raise PermissionDenied

def get_charges(account):
    charges = list(account.charges.all())
    total = round(sum([charge.value for charge in charges]), 2)
    return {"charges": charges, "number": len(charges), "total": total, 'account': account}

@require_http_methods(["POST"])
@transaction.atomic(savepoint=False)
def save_charge(request, account):
    form = ChargeForm(request.POST)
    form.save_if_valid(account)
    return render_account_page

#
# Users page. Render page with list of users
#
@login_required
@require_http_methods(["GET", "POST"])
def render_users_page(request):
    users = list(User.objects.all())
    context = {"users": users, "number": len(users)}
    return render(request, 'finance/users.html', context)
