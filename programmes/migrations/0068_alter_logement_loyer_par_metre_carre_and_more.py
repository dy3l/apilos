# Generated by Django 4.1.6 on 2023-02-10 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "programmes",
            "0067_alter_programme_adresse_alter_programme_code_postal_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="logement",
            name="loyer_par_metre_carre",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                null=True,
                verbose_name="Loyer maximum en € par m² de surface utile",
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="surface_annexes_retenue",
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name="logement",
            name="surface_corrigee",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                null=True,
                verbose_name="Surface corrigée",
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="surface_habitable",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=12,
                null=True,
                verbose_name="Surface habitable",
            ),
        ),
        migrations.AlterField(
            model_name="logement",
            name="surface_utile",
            field=models.DecimalField(
                decimal_places=2, max_digits=12, null=True, verbose_name="Surface utile"
            ),
        ),
        migrations.AlterField(
            model_name="lot",
            name="surface_habitable_totale",
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]
