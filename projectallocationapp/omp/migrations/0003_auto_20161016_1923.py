# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-16 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omp', '0002_auto_20161016_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
