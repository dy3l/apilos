# Generated by Django 3.2.12 on 2022-04-11 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0041_lot_lgts_mixite_sociale_negocies"),
    ]

    operations = [
        migrations.AddField(
            model_name="lot",
            name="loyer_derogatoire",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="Loyer dérogatoire",
            ),
        ),
    ]