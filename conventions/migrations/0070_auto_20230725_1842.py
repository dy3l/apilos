# Generated by Django 4.2.3 on 2023-07-25 16:42

from django.db import migrations


def add_avenant_types(apps, schema_editor):
    AvenantType = apps.get_model("conventions", "AvenantType")
    AvenantType.objects.create(
        nom="denonciation",
        desc="Dénoncer une convention et ses avenants.",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("conventions", "0069_add_data_avenanttype"),
    ]

    operations = [
        migrations.RunPython(add_avenant_types),
    ]