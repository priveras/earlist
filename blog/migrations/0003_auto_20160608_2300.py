# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-09 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160608_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_time',
        ),
        migrations.AddField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(db_index=True, null=True),
        ),
    ]
