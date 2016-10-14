from django.shortcuts import render
from django.http import HttpResponse

from .models import *


def response_info(request):
    context = get_charges()
    return render(request, 'finance/info.html', context)

def response_index(request):
    context = {}
    return render(request, 'finance/index.html', context)

def get_charges():
    charges = []
    for item in Charge.objects.all():
        charges.append(item)
    return {"events": charges, "numbers": len(Charge.objects.all())}
