# Generated by Django 3.2.13 on 2022-07-08 00:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0047_alter_lot_financement"),
        ("conventions", "0024_auto_20220704_0936"),
    ]

    operations = [
        migrations.AlterField(
            model_name="convention",
            name="financement",
            field=models.CharField(
                choices=[
                    ("PLUS", "PLUS"),
                    ("PLAI", "PLAI"),
                    ("PLAI_ADP", "PLAI_ADP"),
                    ("PLUS-PLAI", "PLUS-PLAI"),
                    ("PLS", "PLS"),
                    ("PSH", "PSH"),
                    ("PALULOS", "PALULOS"),
                ],
                default="PLUS",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="convention",
            name="programme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="conventions",
                to="programmes.programme",
            ),
        ),
        migrations.AlterField(
            model_name="convention",
            name="statut",
            field=models.CharField(
                choices=[
                    ("1. Projet", "Création d'un projet de convention"),
                    (
                        "2. Instruction requise",
                        "Projet de convention soumis à l'instruction",
                    ),
                    (
                        "3. Corrections requises",
                        "Projet de convention à modifier par le bailleur",
                    ),
                    ("4. A signer", "Convention à signer"),
                    ("5. Transmise", "Convention transmise"),
                    ("6. Resiliee", "Convention résiliée"),
                ],
                default="1. Projet",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="conventionhistory",
            name="statut_convention",
            field=models.CharField(
                choices=[
                    ("1. Projet", "Création d'un projet de convention"),
                    (
                        "2. Instruction requise",
                        "Projet de convention soumis à l'instruction",
                    ),
                    (
                        "3. Corrections requises",
                        "Projet de convention à modifier par le bailleur",
                    ),
                    ("4. A signer", "Convention à signer"),
                    ("5. Transmise", "Convention transmise"),
                    ("6. Resiliee", "Convention résiliée"),
                ],
                default="1. Projet",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="conventionhistory",
            name="statut_convention_precedent",
            field=models.CharField(
                choices=[
                    ("1. Projet", "Création d'un projet de convention"),
                    (
                        "2. Instruction requise",
                        "Projet de convention soumis à l'instruction",
                    ),
                    (
                        "3. Corrections requises",
                        "Projet de convention à modifier par le bailleur",
                    ),
                    ("4. A signer", "Convention à signer"),
                    ("5. Transmise", "Convention transmise"),
                    ("6. Resiliee", "Convention résiliée"),
                ],
                default="1. Projet",
                max_length=25,
            ),
        ),
    ]
