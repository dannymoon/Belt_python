# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-27 04:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.TextField(max_length=255),
        ),
    ]
