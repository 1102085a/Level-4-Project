# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-24 16:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('omp', '0008_auto_20161024_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='adminID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='project',
            field=models.OneToOneField(default='None', on_delete=django.db.models.deletion.CASCADE, to='omp.Project'),
        ),
        migrations.AlterField(
            model_name='student',
            name='studentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='supervisorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]