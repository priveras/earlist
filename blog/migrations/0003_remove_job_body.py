# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 05:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='body',
        ),
    ]
