# Generated by Django 2.0 on 2017-12-24 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Class_Management', '0005_auto_20171225_0541'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiztimer',
            old_name='time_to_stop',
            new_name='timer',
        ),
    ]
