# Generated by Django 2.0 on 2018-01-01 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assign_Management', '0005_auto_20180101_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='fileUpload',
            field=models.FileField(upload_to='file_uploads'),
        ),
    ]
