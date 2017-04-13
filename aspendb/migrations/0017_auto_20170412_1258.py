# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0016_processactivityreport'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spotcheckreport',
            old_name='time',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='processactivityreport',
            name='timestamp',
            field=models.TimeField(auto_now=True),
        ),
    ]