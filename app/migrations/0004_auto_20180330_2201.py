# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-31 05:01
from __future__ import unicode_literals

from django.db import migrations, models

def update_documented_at(apps, schema_editor):
    Donor = apps.get_model('app', 'Donor')
    for donor in Donor.objects.all():
        donor.documented_at = '%s' % (donor.created_at.strftime("%Y-%m-%d"))
        donor.save()

    Donation = apps.get_model('app', 'Donation')
    for donation in Donation.objects.all():
        donation.documented_at = '%s' % (donation.created_at.strftime("%Y-%m-%d"))
        donation.save()

    Item = apps.get_model('app', 'Item')
    for item in Item.objects.all():
        item.documented_at = '%s' % (item.created_at.strftime("%Y-%m-%d"))
        item.save()

def reverse_update_documented_at(apps, schema_editor):
    # Do nothing since the columns should be deleted anyways
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180328_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='documented_at',
            field=models.CharField(blank=True, max_length=10, verbose_name='Date Created in Y-M-D'),
        ),
        migrations.AddField(
            model_name='donor',
            name='documented_at',
            field=models.CharField(blank=True, max_length=10, verbose_name='Date Created in Y-M-D'),
        ),
        migrations.AddField(
            model_name='item',
            name='documented_at',
            field=models.CharField(blank=True, max_length=10, verbose_name='Date Created in Y-M-D'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='province',
            field=models.CharField(choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('ON', 'Ontario'), ('NS', 'Nova Scotia'), ('NL', 'Newfoundland and Labrador'), ('NU', 'Nunavut'), ('YT', 'Yukon'), ('MB', 'Manitoba'), ('SK', 'Saskatchewan'), ('PE', 'Prince Edward Island'), ('NT', 'Northwest Territories'), ('NB', 'New Brunswick'), ('QC', 'Quebec')], max_length=20, verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(choices=[('Other Printer', 'Other Printer'), ('Camera', 'Camera'), ('CCTV Camera', 'CCTV camera'), ('Speaker', 'Speaker'), ('Other Storage Device', 'Other Storage Device'), ('Keyboard', 'Keyboard'), ('Tablet', 'Tablet'), ('Other gaming console', 'Gaming console'), ('Other', 'Other'), ('Other Network Device', 'Other Network Device'), ('TV', 'Television'), ('Laser Printer', 'Laser Printer'), ('Cables', 'Cables/Connectors'), ('LCD Monitor', 'LCD Monitor'), ('PC-DESKTOP', 'Computer Desktop'), ('Inkjet Printer', 'Inkjet Printer'), ('HeatSink', 'Heat Sink'), ('LED Monitor', 'LED Monitor'), ('SSD', 'Solid State Drive'), ('Xbox', 'Xbox'), ('Fan', 'Fan'), ('RAM', 'Ram'), ('HDD', 'Hard Disk Drive'), ('Router', 'Router'), ('PSU', 'Power Supply'), ('Webcam', 'Webcam'), ('Floppy Drive', 'Floppy Diskette'), ('CPU', 'CPU'), ('Mice', 'Mice'), ('Switch', 'Network Switch'), ('DSLR', 'DSLR'), ('Mobile Phone', 'Mobile Phone'), ('PC-Laptop', 'Computer Laptop'), ('GPU', 'Video Card'), ('Audio Receiver', 'Audio Receiver'), ('Playstation', 'Playstation'), ('HeadPhone', 'Headphones'), ('MotherBoard', 'MotherBoard'), ('LiquidCooler', 'Liquid Cooler'), ('AllInOne Printer', 'All-In-One Printer'), ('Server', 'Server'), ('Other Monitor', 'Other Monitor'), ('3d Printer', '3d Printer'), ('Mic', 'Microphone')], max_length=500, verbose_name='Description'),
        ),
        migrations.RunPython(update_documented_at, reverse_update_documented_at),
    ]
