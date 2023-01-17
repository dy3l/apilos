from django.test import TestCase
from django.urls import reverse

from conventions.tests.views.abstract import AbstractEditViewTestCase
from conventions.tests.fixtures import variantes_success_payload
from programmes.models import NatureLogement


class ConventionVariantesViewTests(AbstractEditViewTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.target_path = reverse(
            "conventions:variantes", args=[self.convention_75.uuid]
        )
        self.next_target_path = reverse(
            "conventions:comments", args=[self.convention_75.uuid]
        )
        self.convention_75.programme.nature_logement = NatureLogement.AUTRE
        self.convention_75.programme.save()
        self.target_template = "conventions/variantes.html"
        self.error_payload = {
            **variantes_success_payload,
            "foyer_variante_2_travaux": "",
        }
        self.success_payload = variantes_success_payload
        self.msg_prefix = "[ConventionVariantesViewTests] "

    def _test_data_integrity(self):
        self.convention_75.refresh_from_db()
        self.assertEqual(
            self.convention_75.foyer_variante_2_travaux,
            "TRAVAUX",
            msg=f"{self.msg_prefix}",
        )