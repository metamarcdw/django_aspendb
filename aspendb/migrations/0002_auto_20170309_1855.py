# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-09 18:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('bad_mix', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('non_fill', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('collapse', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('tears', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('trim', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('voilds', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('open_voilds', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('under_weight', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('over_weight', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Part')),
                ('workcell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='scrap',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='scrap',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='scrap',
            name='part',
        ),
        migrations.RemoveField(
            model_name='scrap',
            name='workcell',
        ),
        migrations.AlterField(
            model_name='downtime',
            name='shift',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3),
        ),
        migrations.AlterField(
            model_name='endofshift',
            name='shift',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3),
        ),
        migrations.AlterField(
            model_name='maintenancerequest',
            name='shift',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3),
        ),
        migrations.AlterField(
            model_name='startofshift',
            name='shift',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3),
        ),
        migrations.DeleteModel(
            name='Scrap',
        ),
        migrations.AlterUniqueTogether(
            name='scrapreport',
            unique_together=set([('date', 'shift', 'workcell', 'part')]),
        ),
    ]
