# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 18:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0007_auto_20170326_0228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapreport',
            name='cracks',
        ),
        migrations.AlterUniqueTogether(
            name='productionschedule',
            unique_together=set([]),
        ),
    ]