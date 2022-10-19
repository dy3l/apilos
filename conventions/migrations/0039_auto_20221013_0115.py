# Generated by Django 4.1.1 on 2022-10-12 23:15

from django.db import migrations


def update_convention_avenanttype(apps, schema_editor):
    Convention = apps.get_model("conventions", "Convention")
    AvenantType = apps.get_model("conventions", "AvenantType")
    logements = AvenantType.objects.get(nom="logements")
    for conventionObj in Convention.objects.all():
        if conventionObj.parent_id:
            conventionObj.avenant_type.add(logements)
        else:
            conventionObj.avenant_type.clear()


class Migration(migrations.Migration):

    dependencies = [
        ("conventions", "0038_load_avenant_type"),
    ]

    operations = [
        migrations.RunPython(update_convention_avenanttype, migrations.RunPython.noop)
    ]
