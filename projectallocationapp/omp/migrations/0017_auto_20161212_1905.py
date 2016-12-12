# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-12 19:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omp', '0016_auto_20161212_1658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='preferences',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name_plural': 'Projects'},
        ),
        migrations.RenameField(
            model_name='administrator',
            old_name='id',
            new_name='adid',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='id',
            new_name='catid',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='id',
            new_name='proid',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='id',
            new_name='stuid',
        ),
        migrations.RenameField(
            model_name='supervisor',
            old_name='id',
            new_name='supid',
        ),
    ]
