# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-25 10:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileattachments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileattachment',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='fileattachment',
            name='update',
        ),
    ]
