# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-11-05 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='people',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('psd', models.CharField(max_length=15)),
            ],
        ),
    ]
