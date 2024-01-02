# Generated by Django 3.2.7 on 2021-09-30 10:03

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UploadedFiles",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("filename", models.CharField(max_length=255, null=True)),
                ("filepath", models.CharField(max_length=255, null=True, unique=True)),
                ("size", models.CharField(max_length=255, null=True)),
                (
                    "thumbnail",
                    models.CharField(blank=True, max_length=100000, null=True),
                ),
            ],
        ),
    ]
