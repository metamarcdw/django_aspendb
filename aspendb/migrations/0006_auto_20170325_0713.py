# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 07:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0005_endofshift_employee_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endofshift',
            name='employee_count',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
