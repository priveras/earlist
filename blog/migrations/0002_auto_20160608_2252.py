# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-09 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='cover_url',
        ),
        migrations.RemoveField(
            model_name='event',
            name='image_url',
        ),
        migrations.AddField(
            model_name='event',
            name='cover_file',
            field=models.FileField(blank=True, upload_to=b'images/%Y%m%d'),
        ),
        migrations.AddField(
            model_name='event',
            name='image_file',
            field=models.FileField(blank=True, upload_to=b'images/%Y%m%d'),
        ),
    ]
