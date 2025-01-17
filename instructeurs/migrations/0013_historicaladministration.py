# Generated by Django 4.1.7 on 2023-04-03 10:20

import uuid

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "instructeurs",
            "0012_rename_signature_label_extra_administration_signature_bloc_signature",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalAdministration",
            fields=[
                ("id", models.IntegerField(blank=True, db_index=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("nom", models.CharField(db_index=True, max_length=255)),
                ("code", models.CharField(db_index=True, max_length=255)),
                ("ville_signature", models.CharField(max_length=255, null=True)),
                ("adresse", models.TextField(blank=True, null=True)),
                ("code_postal", models.CharField(blank=True, max_length=5, null=True)),
                ("ville", models.CharField(blank=True, max_length=255, null=True)),
                ("nb_convention_exemplaires", models.IntegerField(default=3)),
                (
                    "prefix_convention",
                    models.CharField(
                        default="{département}/{zone}/{mois}/{année}/80.416/",
                        max_length=255,
                        null=True,
                    ),
                ),
                ("signataire_bloc_signature", models.TextField(blank=True, null=True)),
                ("cree_le", models.DateTimeField(blank=True, editable=False)),
                ("mis_a_jour_le", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical administration",
                "verbose_name_plural": "historical administrations",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
