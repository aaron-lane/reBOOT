# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-27 02:51
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180506_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='postal_code',
            field=models.CharField(max_length=10, verbose_name='Postal Code'),
        ),
    ]
