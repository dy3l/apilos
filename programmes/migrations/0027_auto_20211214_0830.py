# Generated by Django 3.2.9 on 2021-12-14 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0026_auto_20211202_1232"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lot",
            name="numero",
        ),
        migrations.RemoveField(
            model_name="programme",
            name="departement",
        ),
    ]
