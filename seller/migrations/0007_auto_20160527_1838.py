# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0006_auto_20160527_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='delivery_address',
            field=models.CharField(max_length=500),
        ),
    ]
