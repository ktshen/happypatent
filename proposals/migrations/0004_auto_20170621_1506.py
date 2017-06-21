# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-21 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0003_auto_20170621_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patent',
            name='extended_date',
        ),
        migrations.AddField(
            model_name='patent',
            name='extended_days',
            field=models.IntegerField(blank=True, default=0, verbose_name='Extended Days (days)'),
        ),
    ]