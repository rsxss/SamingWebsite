# Generated by Django 2.0 on 2017-12-24 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class_Management', '0002_auto_20171224_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizscore',
            name='total_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]