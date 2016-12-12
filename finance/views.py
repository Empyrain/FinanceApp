from django.views.decorators.http import *
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Max, Min, Count, Avg

from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

#
# Main page
@require_http_methods(["GET", "POST"])
def render_main_page(request):
    return render(request, 'finance/main.html', {})

#
# Login page
# Render login page with log in forms
#
@require_http_methods(["GET", "POST"])
def render_login_page(request):
    if request.POST.get('username') is not None:
        login_result = log_in(request)
        return login_result
    else:
        return render(request, 'finance/login.html', {})

def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/users/{}'.format(username))
    else:
        context = {'errors': 'Wrong login data. Try again.'}
        return render(request, 'finance/login.html', context)


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
        user = User.objects.create_user(username=username, email=email, password=password)

        profile_form = ProfileForm(request.POST)
        profile = profile_form.save_if_valid(user)
        if profile[0] is True:
            user.save()
            profile[1].save()
            return redirect('login')
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
        save_account(request, request.user)
        context = get_user_and_accounts(request.user)
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
        context['user'] = request.user
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
# Statistic page
# Render page with user finance statisticlist
#
@login_required
@require_http_methods(["GET", "POST"])
def render_statistic_page(request, username):
    if username == request.user.username:
        context = get_statistic_with_class(request.user)
        return render(request, 'finance/statistic.html', context)
    else:
        raise PermissionDenied

def get_statistic_with_class(user):
    statistic = get_statistic()
    statistic.formed_date()
    year_statistics = []
    for date in statistic.date_range_list:
        year_statistics.append(statistic.get_statistic(user, date[0], date[1]))
    return {'year_statistics': year_statistics}

class get_statistic(object):
    ''' Send a requests to database with custom date filters for statistics'''
    def __init__(self):
        self.c_year, self.c_month, self.c_day = datetime.today().year, datetime.today().month, datetime.today().day
        self.o_year, self.o_month, self.o_day = self.get_last_date(self.c_year, self.c_month, self.c_day)
        self.date_range_list = []

    def formed_date(self):
        for i in range(12):
            self.date_range_list.append( [(self.c_year, self.c_month, self.c_day), (self.o_year, self.o_month, self.o_day)] )
            self.c_year, self.c_month, self.c_day = self.get_last_date(self.c_year, self.c_month, self.c_day)
            self.o_year, self.o_month, self.o_day = self.get_last_date(self.o_year, self.o_month, self.o_day)

    def get_statistic(self, user, c_date, o_date):
        now = datetime(c_date[0], c_date[1], c_date[2])
        old = datetime(o_date[0], o_date[1], o_date[2])
        if user.accounts.exists() == True:
            accounts = list(user.accounts.all())
            max_charge, min_charge, number_of_charge, avg = [], [], [], []
            for account in accounts:
                if account.charges.exists() == True:
                    max_charge.append(account.charges.exclude(date__gt=datetime.date(now), date__lt=datetime.date(old)).aggregate(max_charge=Max('value'))['max_charge'])
                    min_charge.append(account.charges.exclude(date__gt=datetime.date(now), date__lt=datetime.date(old)).aggregate(min_charge=Min('value'))['min_charge'])
                    number_of_charge.append(account.charges.exclude(date__gt=datetime.date(now), date__lt=datetime.date(old)).aggregate(n_o_charge=Count('value'))['n_o_charge'])
                    avg.append(account.charges.exclude(date__gt=datetime.date(now), date__lt=datetime.date(old)).aggregate(avg=Avg('value'))['avg'])
                else:
                    max_charge.append(0)
                    min_charge.append(0)
                    number_of_charge.append(0)

            avg = round(float(sum(avg)) / max(len(avg), 1), 2)
            max_charge = max(max_charge)
            min_charge = min(min_charge)
            number_of_charge = sum(number_of_charge)
            latest_charge = account.charges.aggregate(latest_charge=Max('date'))['latest_charge']
            oldest_charge = account.charges.aggregate(oldest_charge=Max('date'))['oldest_charge']
            print(max_charge, min_charge, number_of_charge)
            return {
                'number_of_charge': number_of_charge,
                'max_charge': max_charge,
                'min_charge': min_charge,
                'avg': avg,
                'latest_charge': latest_charge,
                'oldest_charge': oldest_charge
                }
        else:
            return {'errors': 'У вас ещё нет транзакций'}

    def get_last_date(self, year, month, day):
        if month > 1:
            month -= 1
        else:
            year -= 1
            month = 12
        return year, month, day


#
# Users page. Render page with list of users
#
@login_required
@require_http_methods(["GET", "POST"])
def render_users_page(request):
    users = list(User.objects.all())
    context = {"users": users, "number": len(users)}
    return render(request, 'finance/users.html', context)
