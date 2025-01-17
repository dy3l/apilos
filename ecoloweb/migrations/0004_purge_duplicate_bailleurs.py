# Generated by Django 4.1.7 on 2023-04-18 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ecoloweb", "0003_ecolo_ref_est_supprime"),
    ]

    operations = [
        # Purge des références Ecoloweb vers les bailleurs doublons supprimés
        migrations.RunSQL(
            sql="""
delete from ecoloweb_ecoloreference
where
    apilos_model = 'bailleurs.Bailleur'
    and not exists (
        select *
        from bailleurs_bailleur b
        where b.id = apilos_id
    )
        """,
            reverse_sql="",
        )
    ]
