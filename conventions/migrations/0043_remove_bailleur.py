# Generated by Django 4.1.3 on 2022-11-08 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("conventions", "0042_convention_statuts_denoncee_annulee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="convention",
            name="bailleur",
        ),
        migrations.RemoveField(
            model_name="conventionhistory",
            name="bailleur",
        ),
        migrations.RemoveField(
            model_name="pret",
            name="bailleur",
        ),
    ]
