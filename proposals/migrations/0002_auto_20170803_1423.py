# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-03 06:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='employer',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
