from django.http import HttpRequest
from django.test import TestCase

from conventions.models import Convention
from conventions.services import (
    services_logements,
    utils,
)
from core.tests import utils_fixtures
from programmes.forms import TypeStationnementFormSet
from programmes.models import TypeStationnement
from users.models import User


class ConventionTypeStationnementServiceTests(TestCase):
    service_class = services_logements.ConventionTypeStationnementService

    @classmethod
    def setUpTestData(cls):
        utils_fixtures.create_all()

    def setUp(self):
        request = HttpRequest()
        convention = Convention.objects.get(numero="0001")
        request.user = User.objects.get(username="fix")
        self.service = self.service_class(convention=convention, request=request)

    def test_get(self):
        self.service.get()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertIsInstance(self.service.formset, TypeStationnementFormSet)

    def test_save(self):
        self.service.request.POST = {
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 2,
            "form-0-uuid": "",
            "form-0-typologie": "GARAGE_AERIEN",
            "form-0-nb_stationnements": 30,
            "form-0-loyer": "",
            "form-1-uuid": "",
            "form-1-typologie": "GARAGE_ENTERRE",
            "form-1-nb_stationnements": "",
            "form-1-loyer": 100.00,
        }
        self.service.save()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        for form in self.service.formset.forms:
            self.assertTrue(
                form.has_error("loyer") or form.has_error("nb_stationnements")
            )

        self.service.request.POST = {
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 2,
            "form-0-uuid": "",
            "form-0-typologie": "GARAGE_AERIEN",
            "form-0-nb_stationnements": 30,
            "form-0-loyer": 12,
            "form-1-uuid": "",
            "form-1-typologie": "GARAGE_ENTERRE",
            "form-1-nb_stationnements": 5,
            "form-1-loyer": 10.00,
        }

        self.service.save()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.SUCCESS)
        garage_aerien = TypeStationnement.objects.get(
            lot=self.service.convention.lot, typologie="GARAGE_AERIEN"
        )
        self.assertEqual(garage_aerien.nb_stationnements, 30)
        self.assertEqual(garage_aerien.loyer, 12)
        garage_enterre = TypeStationnement.objects.get(
            lot=self.service.convention.lot, typologie="GARAGE_ENTERRE"
        )
        self.assertEqual(garage_enterre.nb_stationnements, 5)
        self.assertEqual(garage_enterre.loyer, 10)