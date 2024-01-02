# Generated by Django 3.2.13 on 2022-07-14 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0048_auto_20220712_2200"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annexe",
            name="logement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="annexes",
                to="programmes.logement",
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="lot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="logements",
                to="programmes.lot",
            ),
        ),
        migrations.AlterField(
            model_name="typestationnement",
            name="lot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="type_stationnements",
                to="programmes.lot",
            ),
        ),
    ]
