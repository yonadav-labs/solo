# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-13 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_remove_seller_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='radius',
            field=models.FloatField(default=10),
        ),
    ]
