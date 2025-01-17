# Generated by Django 4.1.3 on 2022-11-21 10:48

from django.db import migrations, models


def remove_plai_adp(apps, schema_editor):
    LogementEDD = apps.get_model("programmes", "LogementEDD")
    LogementEDD.objects.filter(financement="PLAI_ADP").update(financement="PLAI")


class Migration(migrations.Migration):
    dependencies = [
        ("programmes", "0054_remove_bailleur"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logementedd",
            name="financement",
            field=models.CharField(
                choices=[
                    ("PLUS", "PLUS"),
                    ("PLAI", "PLAI"),
                    ("PLS", "PLS"),
                    ("SANS_FINANCEMENT", "Sans Financement"),
                ],
                default="PLUS",
                max_length=25,
            ),
        ),
        migrations.RunPython(remove_plai_adp, migrations.RunPython.noop),
    ]
