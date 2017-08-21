# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-21 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_auto_20170820_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='controlevent',
            options={'verbose_name': 'Application', 'verbose_name_plural': 'Applications'},
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='proposal_no',
        ),
        migrations.AddField(
            model_name='proposal',
            name='proposal_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='Proposal ID'),
        ),
    ]