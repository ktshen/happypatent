# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-18 10:52
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, max_length=30, unique=True)),
                ('text', ckeditor.fields.RichTextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('update', models.DateTimeField(auto_now=True, null=True, verbose_name='Latest Update')),
            ],
        ),
    ]
