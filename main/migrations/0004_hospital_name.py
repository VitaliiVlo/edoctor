# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-11 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190409_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='name',
            field=models.CharField(default='name', max_length=200),
            preserve_default=False,
        ),
    ]
