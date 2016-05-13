# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-13 02:37
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='longitude/latitude')),
            ],
            managers=[
                ('gis', django.db.models.manager.Manager()),
            ],
        ),
    ]
