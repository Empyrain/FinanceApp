from django.shortcuts import render
from django.http import HttpResponse

from .models import *


def response_info(request):
    # context = get_charges()
    generator = random_transactions()
    context = {"events": generator, "numbers": 'gen hasn\'t len()'}
    return render(request, 'finance/info.html', context)

def response_index(request):
    context = {}
    return render(request, 'finance/index.html', context)

def get_charges():
    charges = []
    for item in Charge.objects.all():
        charges.append(item)
    return {"events": charges, "numbers": len(Charge.objects.all())}


from datetime import date
from decimal import Decimal
from random import randint
def random_transactions():
    today = date.today()
    start_date = today.replace(month=1, day=1).toordinal()
    end_date = today.toordinal()
    while True:
        start_date = randint(start_date, end_date)
        random_date = date.fromordinal(start_date)
        if random_date >= today:
            break
        random_value = randint(-10000, 10000), randint(0, 99)
        random_value = Decimal('%d.%d' % random_value)
        yield random_date, random_value
