# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0018_auto_20170412_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='layeredprocessaudit',
            name='comments',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]