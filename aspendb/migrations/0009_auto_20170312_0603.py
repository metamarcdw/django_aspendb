# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-12 06:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0008_endofshift_scrap_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endofshift',
            name='oee',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='endofshift',
            name='scrap_percent',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]