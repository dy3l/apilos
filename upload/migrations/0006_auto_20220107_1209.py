# Generated by Django 3.2.11 on 2022-01-07 11:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("upload", "0005_alter_uploadedfile_dirpath"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadedfile",
            name="cree_le",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="uploadedfile",
            name="mis_a_jour_le",
            field=models.DateTimeField(auto_now=True),
        ),
    ]