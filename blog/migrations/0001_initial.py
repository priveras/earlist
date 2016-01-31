# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 23:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('body', models.TextField()),
                ('image_url', models.CharField(max_length=500)),
                ('created_at', models.DateField(auto_now_add=True, db_index=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category')),
            ],
        ),
    ]
