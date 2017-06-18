# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-18 06:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('update', models.DateTimeField(auto_now=True, null=True, verbose_name='Latest Update')),
                ('chinese_name', models.CharField(max_length=50, verbose_name='Chinese name')),
                ('english_name', models.CharField(max_length=50, verbose_name='English name')),
                ('country', models.CharField(max_length=50, verbose_name='Country/City')),
                ('post_address', models.CharField(max_length=100, verbose_name='Post Office Address')),
                ('english_address', models.CharField(max_length=100, verbose_name='English Address')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Phone Number')),
                ('id_number', models.CharField(blank=True, max_length=20, verbose_name='ID Number')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='proposals.Client')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='patent',
            name='inventor',
            field=models.ManyToManyField(blank=True, to='proposals.Inventor', verbose_name='Inventor'),
        ),
    ]