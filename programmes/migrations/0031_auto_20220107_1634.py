# Generated by Django 3.2.11 on 2022-01-07 15:34

from django.db import migrations, models


def update_fields_zone_bis(apps, schema_editor):
    Programme = apps.get_model("programmes", "Programme")

    for prog in Programme.objects.all():
        if prog.zone_123 in [1, 2, 3]:
            prog.zone_123_bis = str(prog.zone_123)
        if prog.zone_abc in ["A", "Abis", "B1", "B2", "C"]:
            prog.zone_abc_bis = prog.zone_abc
        prog.save()


def nothing_to_do(apps, schema_editor):
    print("nothing to do")


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0030_alter_programme_type_habitat"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="zone_123_bis",
            field=models.CharField(
                choices=[("1", "01"), ("2", "02"), ("3", "03"), ("1bis", "1bis")],
                default=None,
                max_length=25,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="zone_abc_bis",
            field=models.CharField(
                choices=[
                    ("A", "A"),
                    ("Abis", "Abis"),
                    ("B1", "B1"),
                    ("B2", "B2"),
                    ("C", "C"),
                ],
                default=None,
                max_length=25,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="type_operation",
            field=models.CharField(
                choices=[
                    ("SANSOBJET", "Sans Objet"),
                    ("NEUF", "Construction Neuve"),
                    ("VEFA", "Construction Neuve > VEFA"),
                    ("ACQUIS", "Acquisition"),
                    ("ACQUISAMELIORATION", "Acquisition-Amélioration"),
                    ("REHABILITATION", "Réhabilitation"),
                    ("SANSTRAVAUX", "Sans aide financière (sans travaux)"),
                    ("USUFRUIT", "Usufruit"),
                ],
                default="NEUF",
                max_length=25,
            ),
        ),
        migrations.RunPython(update_fields_zone_bis, nothing_to_do),
    ]