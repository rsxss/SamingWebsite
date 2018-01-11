# Generated by Django 2.0 on 2018-01-03 02:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class_Management', '0015_auto_20180103_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztracker',
            name='quizDoneCount',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
