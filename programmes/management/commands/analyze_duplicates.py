import json
from pprint import pprint
from typing import Any

from django.core.management import BaseCommand
from django.db.models import Count

from programmes.models import Programme


class Command(BaseCommand):
    help = "Analyse les doublons de programme"

    def print_programme_info(self, programme):
        print(
            f"Programme {programme.id} {programme.numero_galion}, {programme.nom}, {programme.bailleur.nom}, {programme.administration.nom}"  # noqa: E501
        )

    def sandbox(self):
        qs = Programme.objects.filter(
            numero_galion="2012DD0060063", parent__isnull=True
        )
        print(qs.count())
        for p in qs.all():
            self.print_programme_info(p)

        my_model_fields = [f.name for f in Programme._meta.fields]
        diff = filter(
            lambda field: getattr(qs[0], field, None) != getattr(qs[1], field, None),
            my_model_fields,
        )
        pprint(list(diff))

    def list_duplicates(self) -> list[dict[str, Any]]:
        qs = (
            Programme.objects.filter(numero_galion__regex=r"^\w{13}$")
            .values("numero_galion")
            .annotate(count=Count("numero_galion"))
            .filter(count__gt=1)
            .order_by("-count")
        )
        return list(qs)

    def handle(self, *args, **options):
        duplicates = self.list_duplicates()

        output_filepath = "/tmp/programme_duplicates.json"
        with open(output_filepath, "w") as f:
            f.write(json.dumps(duplicates, indent=2))

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Une liste des doublons a été crée dans: {output_filepath}"
            )
        )
