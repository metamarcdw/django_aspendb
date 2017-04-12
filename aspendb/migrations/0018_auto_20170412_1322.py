# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 18:22
from __future__ import unicode_literals

import aspendb.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0017_auto_20170412_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='LayeredProcessAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=aspendb.models.get_today, validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('verified_parameters', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('weight_inspection', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('chemicals_tracked', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('components_tracked', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('setup_posted', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('chemicals_correct', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('event_missed_shot', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('demold_criteria', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('demold_ncm', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('mold_release', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('work_instructions', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('proper_equipment', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('trim_criteria', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('inspecting_prior', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('trim_dcm', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('quality_alerts', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('boxes_marked', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('pack_criteria', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('labels_match', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('fifo_product', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('product_tracked', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='LPASafety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=aspendb.models.get_today, validators=[aspendb.models.date_validator])),
                ('ppe', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('ppe_info', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('sds', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('iso_exposure', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee')),
            ],
        ),
        migrations.AddField(
            model_name='layeredprocessaudit',
            name='leader_safety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader_safety', to='aspendb.LPASafety'),
        ),
        migrations.AddField(
            model_name='layeredprocessaudit',
            name='shooter_safety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shooter_safety', to='aspendb.LPASafety'),
        ),
        migrations.AddField(
            model_name='layeredprocessaudit',
            name='table_safety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_safety', to='aspendb.LPASafety'),
        ),
        migrations.AddField(
            model_name='layeredprocessaudit',
            name='trim_safety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trim_safety', to='aspendb.LPASafety'),
        ),
        migrations.AddField(
            model_name='layeredprocessaudit',
            name='workcell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AlterUniqueTogether(
            name='layeredprocessaudit',
            unique_together=set([('date', 'shift', 'workcell')]),
        ),
    ]
