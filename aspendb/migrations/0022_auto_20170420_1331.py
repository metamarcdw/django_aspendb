# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 18:31
from __future__ import unicode_literals

from django.db import migrations

def move_starting_shot(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    SOS = apps.get_model("aspendb", "StartOfShift")
    EOS = apps.get_model("aspendb", "EndOfShift")
    for sos in SOS.objects.all():
        this_eos = EOS.objects.filter(
            date=sos.date).filter(
            shift=sos.shift).filter(
            workcell=sos.workcell)
        if this_eos:
            sos.starting_shot = this_eos[0].starting_shot
            sos.save()

class Migration(migrations.Migration):

    dependencies = [
        ('aspendb', '0021_startofshift_starting_shot'),
    ]

    operations = [
        migrations.RunPython(move_starting_shot),
    ]
