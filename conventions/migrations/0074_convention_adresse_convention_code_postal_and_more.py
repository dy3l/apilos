# Generated by Django 4.2.7 on 2023-12-11 14:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("conventions", "0073_alter_convention_financement_alter_pret_preteur"),
    ]

    operations = [
        migrations.AddField(
            model_name="convention",
            name="adresse",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="code_postal",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="ville",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]