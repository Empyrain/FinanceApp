from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# class User(AbstractUser):
#     class Meta:
#         db_table = "User"
#     surname = models.CharField(max_length=25, blank=False)
#     phone = models.CharField(max_length=11, blank=False, default='00000000000')
#     address = models.CharField(max_length=50, blank=False, default='Terra Incognito')

class User(models.Model):
    class Meta:
        db_table = "User"
    name = models.CharField(max_length=25, blank=False, primary_key=True)
    surname = models.CharField(max_length=25, blank=False)
    phone = models.CharField(max_length=11, blank=False, default='00000000000')
    email = models.CharField(max_length=25, blank=False)
    address = models.CharField(max_length=50, blank=False, default='Terra Incognito')
    password = models.CharField(max_length=50, blank=False, default='Terra Incognito')


class Account(models.Model):
    class Meta:
        db_table = "Account"
    name = models.CharField(max_length=5, blank=False, primary_key=True)
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,    #XXX
        User,
        on_delete=models.CASCADE,
        related_name='accounts',
        blank=True,
        null=True
        )

class Charge(models.Model):
    class Meta:
        db_table = "Charge"
    value = models.FloatField(blank=True, default=0.0)
    date = models.CharField(max_length=22)                 #TODO DATEFIELD
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='charges',
        blank=True,
        null=True
        )
