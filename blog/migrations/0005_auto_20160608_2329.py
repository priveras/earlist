# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-09 04:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160608_2301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='date_time',
            new_name='date_time_field',
        ),
    ]
