# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-03 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_auto_20170627_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patent',
            name='IDS_infomation',
            field=models.TextField(blank=True, verbose_name='IDS Information'),
        ),
    ]
