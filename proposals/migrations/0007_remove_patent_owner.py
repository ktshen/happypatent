# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-21 13:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_auto_20170621_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patent',
            name='owner',
        ),
    ]
