# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 20:54
from __future__ import unicode_literals

import aspendb.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0011_auto_20170404_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downtime',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='endofshift',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='laborallocationreport',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='maintenancerecord',
            name='date_performed',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='maintenancerequest',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='productionschedule',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='scrapreport',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='spotcheckreport',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='spotcheckreport',
            name='packer_initials',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='startofshift',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, validators=[aspendb.models.date_validator]),
        ),
    ]
