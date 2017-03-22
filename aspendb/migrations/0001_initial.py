# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 19:33
from __future__ import unicode_literals

import aspendb.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Downtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('minutes', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='DowntimeCode',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(518), django.core.validators.MinValueValidator(101)])),
                ('description', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('training_level', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='EndOfShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('starting_shot', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('ending_shot', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('scheduled_shots', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('missed_shots', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('total_scrap', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('spray_pots', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3, verbose_name='Is your spray pot topped off?')),
                ('adequate_poly', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Is there an adequate supply of poly?')),
                ('adequate_iso', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Is there an adequate supply of iso?')),
                ('replacement_poly', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3, verbose_name='Is replacement poly agitating?')),
                ('scrap_labeled', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Is all scrap properly labeled?')),
                ('cabinet_stocked', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3, verbose_name='Are all supplies in cell leader cabinet stocked?')),
                ('pot_grounded', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3, verbose_name='Is spray pot ground connected?')),
                ('comments', models.CharField(blank=True, max_length=500)),
                ('total_shots', models.IntegerField()),
                ('oee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('scrap_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[aspendb.models.date_validator], verbose_name='Date performed')),
                ('problem_code', models.CharField(choices=[('mech', 'Mechanical'), ('elec', 'Electrical'), ('pneu', 'Pneumatic'), ('hydr', 'Hydraulic'), ('water', 'Water'), ('struc', 'Structural'), ('chem', 'Chemical')], max_length=5)),
                ('work_done', models.CharField(blank=True, max_length=50)),
                ('repair_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('workcell_downtime', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('parts_used', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('parts_reordered', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3)),
                ('parts_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee', verbose_name='Work performed by')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('problem', models.CharField(max_length=100)),
                ('urgency', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('status', models.CharField(choices=[('open', 'Open'), ('completed', 'Completed')], default='open', max_length=30)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to='aspendb.Employee')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to='aspendb.Employee')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Department')),
                ('record', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aspendb.MaintenanceRecord')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('part_number', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('hours', models.DecimalField(decimal_places=2, default=10, max_digits=4)),
                ('shots', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Shots per round')),
                ('total_shots', models.IntegerField()),
                ('part', smart_selects.db_fields.ChainedForeignKey(chained_field='workcell', chained_model_field='workcell', on_delete=django.db.models.deletion.CASCADE, to='aspendb.Part')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('bad_mix', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('dents', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('mold_release', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('non_fill', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('collapse', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('tears', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('trim', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('voilds', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('open_voilds', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('under_weight', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('over_weight', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('total_scrap', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('numbers', models.TextField(max_length=1000)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee')),
                ('part', smart_selects.db_fields.ChainedForeignKey(chained_field='workcell', chained_model_field='workcell', on_delete=django.db.models.deletion.CASCADE, to='aspendb.Part')),
            ],
        ),
        migrations.CreateModel(
            name='StartOfShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[aspendb.models.date_validator])),
                ('shift', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd')], max_length=3)),
                ('process_verified', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Process parameters verified?')),
                ('weights_verified', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Shot weights verified?')),
                ('mix_ratio', models.FloatField(validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)])),
                ('poly_temp', models.FloatField(validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(60)])),
                ('iso_temp', models.FloatField(validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(60)])),
                ('poly_flow', models.FloatField(validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(20)])),
                ('iso_flow', models.FloatField(validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(20)])),
                ('poly_pressure', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2500), django.core.validators.MinValueValidator(500)])),
                ('iso_pressure', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2500), django.core.validators.MinValueValidator(500)])),
                ('adequate_components', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3, verbose_name='Is there an adequate supply of components?')),
                ('airhose_secure', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3, verbose_name='Are all air hose nozzles secure?')),
                ('poly_agitator', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Is poly agitator functioning?')),
                ('chemical_tracked', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')], max_length=3, verbose_name='Is poly/iso recorded in lot tracking book?')),
                ('poly_date', models.DateField()),
                ('iso_date', models.DateField()),
                ('stands_labels', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Are all pack stands/pack instructions & barcode labels in place?')),
                ('new_product', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Are there any NEW production parts scheduled to run today?')),
                ('opposite_parts', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Are the NEW parts - symetrically opposite parts on the same turntable?')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Workcell',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, validators=[aspendb.models.nospace_validator])),
                ('foam_system', models.CharField(max_length=30)),
                ('turns_per_hour', models.DecimalField(decimal_places=2, default=10, max_digits=4)),
                ('cell_leader_1st', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell_leader_1st', to='aspendb.Employee')),
                ('cell_leader_2nd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell_leader_2nd', to='aspendb.Employee')),
            ],
        ),
        migrations.AddField(
            model_name='startofshift',
            name='workcell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AddField(
            model_name='scrapreport',
            name='workcell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AddField(
            model_name='productionschedule',
            name='workcell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AddField(
            model_name='part',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Program'),
        ),
        migrations.AddField(
            model_name='part',
            name='workcell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='workcell',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AddField(
            model_name='endofshift',
            name='workcell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together=set([('first_name', 'last_name')]),
        ),
        migrations.AddField(
            model_name='downtime',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.DowntimeCode'),
        ),
        migrations.AddField(
            model_name='downtime',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Employee'),
        ),
        migrations.AddField(
            model_name='downtime',
            name='workcell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aspendb.Workcell'),
        ),
        migrations.AlterUniqueTogether(
            name='startofshift',
            unique_together=set([('date', 'shift', 'workcell')]),
        ),
        migrations.AlterUniqueTogether(
            name='scrapreport',
            unique_together=set([('date', 'shift', 'workcell', 'part')]),
        ),
        migrations.AlterUniqueTogether(
            name='productionschedule',
            unique_together=set([('date', 'shift', 'workcell', 'part')]),
        ),
        migrations.AlterUniqueTogether(
            name='endofshift',
            unique_together=set([('date', 'shift', 'workcell')]),
        ),
    ]
