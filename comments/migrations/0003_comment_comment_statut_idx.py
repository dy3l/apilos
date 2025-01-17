# Generated by Django 4.2.7 on 2023-12-06 14:06

from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("comments", "0002_alter_comment_uuid_objet"),
    ]

    operations = [
        AddIndexConcurrently(
            model_name="comment",
            index=models.Index(fields=["statut"], name="comment_statut_idx"),
        ),
    ]
