# Generated by Django 3.2.9 on 2021-12-14 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0027_auto_20211214_0830"),
    ]

    operations = [
        migrations.RenameField(
            model_name="programme",
            old_name="autre_locaux_hors_convention",
            new_name="autres_locaux_hors_convention",
        ),
    ]
