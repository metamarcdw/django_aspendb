# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 19:34
from __future__ import unicode_literals

import aspendb.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0025_auto_20170426_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaborReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=aspendb.models.get_today, validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('man_hours', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee')),
                ('workcell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='laborreport',
            unique_together=set([('date', 'shift', 'workcell')]),
        ),
    ]
