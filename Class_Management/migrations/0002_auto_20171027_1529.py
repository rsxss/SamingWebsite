# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class_Management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quizDetail',
            field=models.CharField(max_length=1024),
        ),
    ]
