# Generated by Django 2.0 on 2017-12-25 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class_Management', '0007_auto_20171225_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiztimer',
            name='start',
            field=models.BooleanField(default=False),
        ),
    ]
