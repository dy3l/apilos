# Generated by Django 3.2.14 on 2022-09-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("programmes", "0052_auto_20220722_0627"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logement",
            name="typologie",
            field=models.CharField(
                choices=[
                    ("T1", "T1"),
                    ("T1bis", "T1bis"),
                    ("T2", "T2"),
                    ("T3", "T3"),
                    ("T4", "T4"),
                    ("T5", "T5"),
                    ("T6", "T6 et plus"),
                ],
                default="T1",
                max_length=25,
            ),
        ),
    ]
