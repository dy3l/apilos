# Generated by Django 3.2.14 on 2022-07-22 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0051_alter_typestationnement_typologie"),
    ]

    operations = [
        migrations.AddField(
            model_name="lot",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="programmes.lot",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="programmes.programme",
            ),
        ),
    ]
