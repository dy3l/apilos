# Generated by Django 4.1.3 on 2022-12-06 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0057_alter_programme_nature_logement"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="date_autorisation_hors_habitat_inclusif",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="programme",
            name="date_convention_location",
            field=models.DateField(null=True),
        ),
    ]