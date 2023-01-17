# Generated by Django 4.1.3 on 2022-12-06 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0056_alter_logementedd_programme_alter_lot_programme_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programme",
            name="nature_logement",
            field=models.CharField(
                choices=[
                    ("LOGEMENTSORDINAIRES", "Logements ordinaires"),
                    ("AUTRE", "Autres logements foyers"),
                    ("HEBERGEMENT", "Hébergement"),
                    ("RESISDENCESOCIALE", "Résidence sociale"),
                    ("PENSIONSDEFAMILLE", "Pensions de famille (Maisons relais)"),
                    ("RESIDENCEDACCUEIL", "Résidence d'accueil"),
                    ("RESIDENCEUNIVERSITAIRE", "Résidence universitaire"),
                    ("RHVS", "RHVS"),
                ],
                default="LOGEMENTSORDINAIRES",
                max_length=25,
            ),
        ),
    ]