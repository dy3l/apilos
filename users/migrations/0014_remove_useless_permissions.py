# Generated by Django 3.2.14 on 2022-09-26 16:14

from django.db import migrations


def recreate_useless_permissions(apps, schema_editor):
    pass


def delete_useless_permissions(apps, schema_editor):
    # Delete useless permissions
    Permission = apps.get_model("auth", "Permission")
    Permission.objects.filter(content_type__app_label="django_docx_template").delete()

    # Delete the 'django_docx_template' content type
    ContentType = apps.get_model("contenttypes", "ContentType")
    ContentType.objects.filter(app_label="django_docx_template").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_auto_20220906_1022"),
    ]

    operations = [
        migrations.RunPython(
            delete_useless_permissions, reverse_code=recreate_useless_permissions
        )
    ]
