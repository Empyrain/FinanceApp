# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-14 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Account',
            },
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('charge_id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.IntegerField()),
                ('date', models.CharField(default='42', max_length=4)),
            ],
            options={
                'db_table': 'Charge',
            },
        ),
    ]
