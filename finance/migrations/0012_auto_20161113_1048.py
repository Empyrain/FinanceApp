# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-13 10:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_auto_20161113_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='account',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='finance.Account'),
        ),
    ]