# Generated by Django 3.2.12 on 2022-04-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conventions", "0018_convention_type1and2"),
    ]

    operations = [
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option1",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option2",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option3",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option4",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option5",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option6",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option7",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="convention",
            name="type2_lgts_concernes_option8",
            field=models.BooleanField(default=True),
        ),
    ]