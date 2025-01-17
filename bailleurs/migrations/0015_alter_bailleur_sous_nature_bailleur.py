# Generated by Django 4.1.5 on 2023-01-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bailleurs", "0014_alter_bailleur_capital_social_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bailleur",
            name="sous_nature_bailleur",
            field=models.CharField(
                choices=[
                    ("ASSOCIATIONS", "Associations"),
                    ("ANAH", "ANAH"),
                    ("COMMERCIALES", "entreprises commerciales"),
                    ("COMMUNE", "Commune"),
                    ("COOPERATIVE_HLM_SCIC", "Sté coopérative HLM /SCIC"),
                    ("CROUS", "CROUS"),
                    ("DEPARTEMENT", "Département"),
                    ("DRE_DDE_CETE_AC_PREF", "DRE,DDE,CETE,AC,Préfect."),
                    ("EPCI", "EPCI"),
                    ("ETC_PUBLIQUE_LOCAL", "Ets public local"),
                    ("ETS_HOSTIPATIERS_PRIVES", "Ets hospitaliers privés"),
                    ("FONDATION", "Fondation"),
                    ("FONDATION_HLM", "Fondation HLM"),
                    ("FRONCIERE_LOGEMENT", "Foncière Logement"),
                    ("GIP", "GIP"),
                    ("MUTUELLE", "Mutuelle"),
                    ("NONRENSEIGNE", "Non renseigné"),
                    ("OFFICE_PUBLIC_HLM", "Office public HLM (OPH)"),
                    ("PACT_ARIM", "Pact-Arim"),
                    ("PARTICULIERS", "Particuliers"),
                    ("SA_HLM_ESH", "SA HLM / ESH"),
                    ("SACI_CAP", "SACI CAP"),
                    ("SEM_EPL", "SEM / EPL"),
                    ("UES", "UES"),
                ],
                default="NONRENSEIGNE",
                max_length=25,
            ),
        ),
    ]
