# Generated by Django 4.2.1 on 2023-07-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("conventions", "0067_convention_unique_display_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="convention",
            name="champ_libre_avenant",
            field=models.TextField(blank=True, null=True),
        ),
    ]
