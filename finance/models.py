from django.db import models
from django import forms

class Charge(models.Model):
    '''Денежная транзакция'''
    class Meta:
        db_table = "Charge"
    charge_id = models.AutoField(primary_key=True)
    value = models.FloatField(blank=False)
    date = models.CharField(max_length=22)
    # account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Account(models.Model):
    '''Банковский счёт'''
    class Meta:
        db_table = "Account"
    total = models.IntegerField(blank=False, default=0)
