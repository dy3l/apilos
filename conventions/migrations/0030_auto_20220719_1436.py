# Generated by Django 3.2.13 on 2022-07-19 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("conventions", "0029_auto_20220718_1427"),
    ]

    operations = [
        migrations.AddField(
            model_name="convention",
            name="avenant_type",
            field=models.CharField(
                choices=[
                    ("1. Programme", "Modification du programme"),
                    ("2. Travaux", "Travaux, réhabilitation totale"),
                    (
                        "3. Prorogation",
                        "Prorogation de la durée de la convention suite à travaux financés",
                    ),
                    (
                        "4. Mutation",
                        "Vente ou changement de dénomination du propriétaire",
                    ),
                    ("5. Gestionnaire", "Changement de gestionnaire (pour les foyers)"),
                    ("6. Loyer Maximum", "Modification du loyer maximum"),
                    ("7. Dénonciation", "Dénonciation partielle"),
                ],
                default="1. Programme",
                max_length=25,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="convention",
            name="parent_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="avenants",
                to="conventions.convention",
            ),
        ),
    ]