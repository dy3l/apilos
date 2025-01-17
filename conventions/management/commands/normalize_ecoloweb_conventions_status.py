import argparse
import logging
from datetime import date

from django.core.management.base import BaseCommand

from conventions.models import Convention
from conventions.models.choices import ConventionStatut
from ecoloweb.models import EcoloReference

logger = logging.getLogger(__name__)
THRESHOLD_DATE = date(2023, 3, 1)


def find_ecoloweb_conventions():
    ecoloweb_conventions_ids = EcoloReference.objects.filter(
        apilos_model="conventions.Convention"
    ).values_list("apilos_id", flat=True)

    base_queryset = Convention.objects.filter(
        statut__in=[
            ConventionStatut.PROJET.label,
            ConventionStatut.INSTRUCTION.label,
            ConventionStatut.CORRECTION.label,
            ConventionStatut.A_SIGNER.label,
        ]
    ).filter(id__in=ecoloweb_conventions_ids)
    before_conventions = base_queryset.filter(
        televersement_convention_signee_le__lte=THRESHOLD_DATE,
    )
    after_conventions = base_queryset.filter(
        televersement_convention_signee_le__gt=THRESHOLD_DATE
    )

    return before_conventions, after_conventions


def update_conventions_status(conventions):
    conventions.update(statut=ConventionStatut.SIGNEE.label)
    logger.warning("%s conventions ont été mises à jour au statut Signée")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            help="Run command and write changes to the database",
            action=argparse.BooleanOptionalAction,
            default=False,
        )

        parser.add_argument(
            "--verbose",
            help="Print all conventions",
            action=argparse.BooleanOptionalAction,
            default=False,
        )

        parser.add_argument(
            "--before",
            help="update conventions before the 1th of March 2023",
            action=argparse.BooleanOptionalAction,
            default=False,
        )

        parser.add_argument(
            "--after",
            help="update conventions after the 1th of March 2023",
            action=argparse.BooleanOptionalAction,
            default=False,
        )

    def handle(self, *args, **options):
        verbose = options.get("verbose")
        dry_run = options.get("dry_run")
        before = options.get("before")
        after = options.get("after")

        if not dry_run:
            logger.warning(
                "La commande n'a pas été lancée avec le mode dry_run, des données vont être écrites en base de données"
            )

        before_conventions, after_conventions = find_ecoloweb_conventions()

        if before:
            logger.warning(
                "%s conventions antérieures au 1er mars 2023 concernées",
                len(before_conventions),
            )
            if verbose:
                for convention in before_conventions:
                    logger.warning(convention)

            if not dry_run:
                update_conventions_status(before_conventions)

        if after:
            logger.warning(
                "%s conventions postérieures au 1er mars 2023 concernées",
                len(after_conventions),
            )
            if verbose:
                for convention in after_conventions:
                    logger.warning(convention)

            if not dry_run:
                update_conventions_status(after_conventions)
