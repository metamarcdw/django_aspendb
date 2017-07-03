class Migration(migrations.Migration):

    def fill_all_ids(apps, schema_editor):
        def fill_id_field(model):
            num = 1
            for row in model.objects.all():
                row.id = num
                row.save()
                num += 1

        fill_id_field(apps.get_model('aspendb', 'Department'))
        fill_id_field(apps.get_model('aspendb', 'Program'))
        fill_id_field(apps.get_model('aspendb', 'Workcell'))
        fill_id_field(apps.get_model('aspendb', 'Part'))
        fill_id_field(apps.get_model('aspendb', 'DowntimeCode'))

    operations = [
        migrations.RunPython(fill_all_ids),
    ]
