# Generated by Django 3.2.10 on 2022-01-03 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_cerbere_uid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="cerbere_uid",
        ),
    ]