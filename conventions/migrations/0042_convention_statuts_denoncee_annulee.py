# Generated by Django 4.1.3 on 2022-11-07 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conventions', '0037_avenanttype_remove_convention_avenant_type_and_more_squashed_0041_alter_convention_avenant_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='statut',
            field=models.CharField(choices=[('1. Projet', "Création d'un projet de convention"), ('2. Instruction requise', "Projet de convention soumis à l'instruction"), ('3. Corrections requises', 'Projet de convention à modifier par le bailleur'), ('4. A signer', 'Convention à signer'), ('5. Signée', 'Convention signée'), ('6. Résiliée', 'Convention résiliée'), ('7. Dénoncée', 'Convention dénoncée'), ('8. Annulée en suivi', 'Convention annulée en suivi')], default='1. Projet', max_length=25),
        ),
        migrations.AlterField(
            model_name='conventionhistory',
            name='statut_convention',
            field=models.CharField(choices=[('1. Projet', "Création d'un projet de convention"), ('2. Instruction requise', "Projet de convention soumis à l'instruction"), ('3. Corrections requises', 'Projet de convention à modifier par le bailleur'), ('4. A signer', 'Convention à signer'), ('5. Signée', 'Convention signée'), ('6. Résiliée', 'Convention résiliée'), ('7. Dénoncée', 'Convention dénoncée'), ('8. Annulée en suivi', 'Convention annulée en suivi')], default='1. Projet', max_length=25),
        ),
        migrations.AlterField(
            model_name='conventionhistory',
            name='statut_convention_precedent',
            field=models.CharField(choices=[('1. Projet', "Création d'un projet de convention"), ('2. Instruction requise', "Projet de convention soumis à l'instruction"), ('3. Corrections requises', 'Projet de convention à modifier par le bailleur'), ('4. A signer', 'Convention à signer'), ('5. Signée', 'Convention signée'), ('6. Résiliée', 'Convention résiliée'), ('7. Dénoncée', 'Convention dénoncée'), ('8. Annulée en suivi', 'Convention annulée en suivi')], default='1. Projet', max_length=25),
        ),
    ]