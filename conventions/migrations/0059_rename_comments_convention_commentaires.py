# Generated by Django 4.1.5 on 2023-02-05 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("conventions", "0058_piece_jointe_max_lengths"),
    ]

    operations = [
        migrations.RenameField(
            model_name="convention",
            old_name="comments",
            new_name="commentaires",
        ),
    ]
