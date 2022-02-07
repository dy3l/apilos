# Generated by Django 3.2.11 on 2022-02-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0034_auto_20220119_1150"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logement",
            name="coeficient",
            field=models.DecimalField(
                decimal_places=4,
                max_digits=6,
                null=True,
                verbose_name="Coefficient propre au logement",
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="designation",
            field=models.CharField(
                max_length=255, verbose_name="Désignation des logements"
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="loyer_par_metre_carre",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="Loyer maximum en € par m² de surface utile",
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="surface_habitable",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="Surface habitable",
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="surface_utile",
            field=models.DecimalField(
                decimal_places=2, max_digits=6, null=True, verbose_name="Surface utile"
            ),
        ),
    ]