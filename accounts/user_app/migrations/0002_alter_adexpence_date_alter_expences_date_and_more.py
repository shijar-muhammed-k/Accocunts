# Generated by Django 4.2.3 on 2023-07-21 18:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adexpence',
            name='Date',
            field=models.DateField(default=datetime.datetime(2023, 7, 22, 0, 19, 9, 80823)),
        ),
        migrations.AlterField(
            model_name='expences',
            name='Date',
            field=models.DateField(default=datetime.datetime(2023, 7, 22, 0, 19, 9, 80823)),
        ),
        migrations.AlterField(
            model_name='returns',
            name='Date',
            field=models.DateField(default=datetime.datetime(2023, 7, 22, 0, 19, 9, 80823)),
        ),
        migrations.AlterField(
            model_name='sales',
            name='Date',
            field=models.DateField(default=datetime.datetime(2023, 7, 22, 0, 19, 9, 80823)),
        ),
    ]
