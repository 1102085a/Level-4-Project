# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-13 11:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omp', '0017_auto_20161212_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='catid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='proid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='stuid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='supervisor',
            old_name='supid',
            new_name='id',
        ),
    ]
