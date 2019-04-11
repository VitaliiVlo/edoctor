# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-11 12:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190411_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='visits_doctor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
