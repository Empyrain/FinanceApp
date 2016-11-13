from django.db import models
from django import forms

class Account(models.Model):
    class Meta:
        db_table = "Account"
    name = models.CharField(max_length=16, blank=False, primary_key=True)
    last_name = models.CharField(max_length=16, blank=False)
    email = models.EmailField(max_length=70,blank=False, default='-@-.ru')
    total = models.IntegerField(blank=False, default=0)


class Charge(models.Model):
    class Meta:
        db_table = "Charge"
    value = models.FloatField(blank=True, default=0.0)
    date = models.CharField(max_length=22)                                       #XXX DATEFIELD
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='charges',
        blank=True,
        null=True
        )
