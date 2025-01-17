# Generated by Django 4.2 on 2023-05-15 17:12

from django.db import migrations

from programmes.models import Financement


def remove_unknown_financement(apps, schema_editor):
    Lot = apps.get_model("programmes", "Lot")
    Lot.objects.exclude(financement__in=Financement.values).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("programmes", "0076_loyers_indices_over_periods"),
    ]

    operations = [
        migrations.RunPython(remove_unknown_financement, migrations.RunPython.noop),
    ]
