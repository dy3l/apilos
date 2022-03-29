# Generated by Django 3.2.12 on 2022-03-29 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apilos_settings", "0002_auto_20220317_1211"),
        ("users", "0008_user_filtre_departements"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="filtre_departements",
            field=models.ManyToManyField(
                blank=True,
                help_text="Les programmes et conventions affichés à l'utilisateur seront filtrés en utilisant la liste des départements ci-dessous",
                related_name="filtre_departements",
                to="apilos_settings.Departement",
            ),
        ),
    ]