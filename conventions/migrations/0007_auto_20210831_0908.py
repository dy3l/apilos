# Generated by Django 3.2.5 on 2021-08-31 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conventions", "0006_alter_pret_preteur"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pret",
            name="numero",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="pret",
            name="preteur",
            field=models.CharField(
                choices=[
                    ("ETAT", "Etat"),
                    ("EPCI", "EPCI"),
                    ("REGION", "Région"),
                    ("CDCF", "CDC froncière"),
                    ("CDCL", "CDC locative"),
                    ("AUTRE", "Autre"),
                ],
                default="AUTRE",
                max_length=25,
            ),
        ),
    ]
