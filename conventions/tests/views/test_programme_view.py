from django.test import TestCase
from django.urls import reverse

from conventions.tests.views.abstract import AbstractViewTestCase


class ConventionProgrammeViewTests(AbstractViewTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.target_path = reverse(
            "conventions:programme", args=[self.convention_75.uuid]
        )
        self.next_target_path = reverse(
            "conventions:cadastre", args=[self.convention_75.uuid]
        )
        self.target_template = "conventions/programme.html"
        self.error_payload = {
            "nom": "Fake Opération",
            "adresse": "",
            "code_postal": "00000",
            "ville": "Fake ville",
            "nb_logements": "28",
            "anru": "FALSE",
            "type_habitat": "INDIVIDUEL",
            "type_operation": "NEUF",
            "nb_locaux_commerciaux": "",
            "nb_bureaux": "",
            "autres_locaux_hors_convention": "",
        }
        self.success_payload = {
            "nom": "Fake Opération",
            "adresse": "123 rue du fake",
            "code_postal": "00000",
            "ville": "Fake ville",
            "nb_logements": "28",
            "anru": "FALSE",
            "type_habitat": "INDIVIDUEL",
            "type_operation": "NEUF",
            "nb_locaux_commerciaux": "",
            "nb_bureaux": "",
            "autres_locaux_hors_convention": "",
        }
        self.msg_prefix = "[ConventionProgrammeViewTests] "

    def _test_data_integrity(self):
        self.convention_75.refresh_from_db()
        self.assertEqual(
            self.convention_75.programme.adresse,
            "123 rue du fake",
            msg=f"{self.msg_prefix}",
        )