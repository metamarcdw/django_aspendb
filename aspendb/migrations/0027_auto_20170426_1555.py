# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0026_auto_20170426_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laborreport',
            name='employee',
        ),
        migrations.AddField(
            model_name='laborreport',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
