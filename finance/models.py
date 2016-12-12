from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    class Meta:
        db_table = "Profile"
    name = models.CharField(max_length=25, blank=True)
    surname = models.CharField(max_length=25, blank=True)
    phone = models.CharField(max_length=11, blank=False, default='00000000000')
    address = models.CharField(max_length=50, blank=False, default='Terra Incognito')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )

class Account(models.Model):
    class Meta:
        db_table = "Account"
    name = models.CharField(max_length=5, blank=False, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
        blank=True,
        null=True
        )

class Charge(models.Model):
    class Meta:
        db_table = "Charge"
    value = models.FloatField(blank=True, default=0.0)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='charges',
        blank=True,
        null=True
        )
