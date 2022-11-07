# Generated by Django 4.1.1 on 2022-10-10 14:46

from django.db import migrations
from django.db.migrations import RunSQL


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        RunSQL(
            sql="""
create or replace view v_convention_departement
as
select
    c.id,
    asd.id as departement_id
from conventions_convention c
    inner join programmes_programme pp on c.programme_id = pp.id
    inner join apilos_settings_departement asd on substr(pp.code_postal, 1, 2) = asd.code_insee or substr(pp.code_postal, 1, 3) = asd.code_insee
    """,
            reverse_sql="""
drop view if exists v_convention_departement
    """
        ),
        RunSQL(
            sql="""
create or replace view v_convention_statuts
as
select distinct(statut_convention) as statut
from conventions_conventionhistory
    """,
            reverse_sql="""
drop view if exists v_convention_statuts
        """)
    ]