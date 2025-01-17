# Generated by Django 4.1.4 on 2022-12-19 13:33

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0059_lot_surface_habitable_totale_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lot",
            name="foyer_residence_dependance",
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="foyer_residence_locaux_hors_convention",
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="foyer_residence_nb_garage_parking",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="LocauxCollectifs",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("type_local", models.TextField()),
                (
                    "surface_habitable",
                    models.DecimalField(decimal_places=2, max_digits=6),
                ),
                ("nombre", models.IntegerField()),
                ("cree_le", models.DateTimeField(auto_now_add=True)),
                ("mis_a_jour_le", models.DateTimeField(auto_now=True)),
                (
                    "lot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locaux_collectifs",
                        to="programmes.lot",
                    ),
                ),
            ],
        ),
    ]
