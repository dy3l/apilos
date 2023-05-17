# Generated by Django 3.2.11 on 2022-01-11 10:10

from django.db import migrations, models


def update_date_achevement_compile(apps, schema_editor):
    Programme = apps.get_model("programmes", "Programme")

    for prog in Programme.objects.all():
        prog.date_achevement_compile = (
            prog.date_achevement or prog.date_achevement_previsible
        )
        prog.save()


class Migration(migrations.Migration):
    dependencies = [
        ("programmes", "0031_auto_20220107_1634"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="date_achevement_compile",
            field=models.DateField(null=True),
        ),
        migrations.RunPython(update_date_achevement_compile, migrations.RunPython.noop),
    ]
