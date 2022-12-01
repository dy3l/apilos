import mock

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from bailleurs.models import Bailleur
from conventions.models import Convention
from conventions.services import (
    services_programmes,
    utils,
)
from core.tests import utils_fixtures
from instructeurs.models import Administration
from programmes.subforms.lot_selection import (
    ProgrammeSelectionFromDBForm,
    ProgrammeSelectionFromZeroForm,
)
from programmes.models import Financement, Lot, TypeHabitat
from users.models import GroupProfile, User


class ConventionSelectionServiceForInstructeurTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        utils_fixtures.create_all()

    def setUp(self):
        self.request = RequestFactory().get("/conventions/selection")
        self.request.user = User.objects.get(username="fix")
        get_response = mock.MagicMock()
        middleware = SessionMiddleware(get_response)
        middleware.process_request(self.request)
        self.request.session.save()
        self.request.session["currently"] = GroupProfile.INSTRUCTEUR
        self.service = services_programmes.ConventionSelectionService(
            request=self.request
        )

    def test_get_from_db(self):
        administration = Administration.objects.get(code="75000")
        lots = (
            Lot.objects.filter(programme__administration=administration)
            .order_by(
                "programme__ville", "programme__nom", "nb_logements", "financement"
            )
            .filter(programme__parent_id__isnull=True)
        )
        self.service.get_from_db()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertIsInstance(self.service.form, ProgrammeSelectionFromDBForm)
        self.assertEqual(
            self.service.form.declared_fields["lot"].choices,
            [(lot.uuid, str(lot)) for lot in lots],
        )

    def test_post_from_db_failed_form(self):
        self.service.request.POST = {"lot": ""}
        self.service.post_from_db()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("lot"))

    def test_post_from_db_failed_scope(self):
        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="12345")
        programme = utils_fixtures.create_programme(
            bailleur, administration, nom="Programme failed"
        )
        utils_fixtures.create_lot(programme, Financement.PLAI)
        lot_plus = utils_fixtures.create_lot(programme, Financement.PLUS)
        self.service.request.POST = {"lot": str(lot_plus.uuid)}
        self.service.post_from_db()

        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("lot"))

    def test_post_from_db_success(self):
        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="75000")
        programme_2 = utils_fixtures.create_programme(
            bailleur, administration, nom="Programme 2"
        )
        utils_fixtures.create_lot(programme_2, Financement.PLAI)
        lot_plus_2 = utils_fixtures.create_lot(programme_2, Financement.PLUS)

        self.service.request.POST = {"lot": str(lot_plus_2.uuid)}
        self.service.post_from_db()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.SUCCESS)
        self.assertEqual(
            self.service.convention, Convention.objects.get(lot=lot_plus_2)
        )

    def test_get_from_zero(self):
        administration = Administration.objects.get(code="75000")
        bailleurs = Bailleur.objects.all().order_by("nom")
        self.service.get_from_zero()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertIsInstance(self.service.form, ProgrammeSelectionFromZeroForm)
        self.assertEqual(
            self.service.form.declared_fields["administration"].choices,
            [(administration.uuid, str(administration))],
        )
        self.assertEqual(
            self.service.form.declared_fields["bailleur"].choices,
            [(bailleur.uuid, str(bailleur)) for bailleur in bailleurs],
        )

    def test_post_from_zero_failed_form(self):
        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="75000")
        self.service.request.POST = {
            "bailleur": str(bailleur.uuid),
            "administration": str(administration.uuid),
            "nom": "Programme de test",
            "nb_logements": "10",
            "type_habitat": TypeHabitat.MIXTE,
            "financement": Financement.PLUS,
            "code_postal": "20000",
            "ville": "",
        }
        self.service.post_from_zero()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("ville"))

    def test_post_from_zero_failed_scope(self):
        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="12345")
        self.service.request.POST = {
            "bailleur": str(bailleur.uuid),
            "administration": str(administration.uuid),
            "nom": "Programme de test",
            "nb_logements": "10",
            "type_habitat": TypeHabitat.MIXTE,
            "financement": Financement.PLUS,
            "code_postal": "20000",
            "ville": "Bisouville",
        }
        self.service.post_from_zero()

        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("administration"))

    def test_post_from_zero_success(self):
        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="75000")
        self.service.request.POST = {
            "bailleur": str(bailleur.uuid),
            "administration": str(administration.uuid),
            "nom": "Programme de test",
            "nb_logements": "10",
            "type_habitat": TypeHabitat.MIXTE,
            "financement": Financement.PLUS,
            "code_postal": "20000",
            "ville": "Bisouville",
        }
        self.service.post_from_zero()

        self.assertEqual(self.service.return_status, utils.ReturnStatus.SUCCESS)
        self.assertEqual(
            self.service.convention,
            Convention.objects.get(
                programme__nom="Programme de test", financement=Financement.PLUS
            ),
        )


class ConventionSelectionServiceForBailleurTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        utils_fixtures.create_all()

    def setUp(self):
        self.request = RequestFactory().get("/conventions/selection")
        self.request.user = User.objects.get(username="raph")
        get_response = mock.MagicMock()
        middleware = SessionMiddleware(get_response)
        middleware.process_request(self.request)
        self.request.session.save()
        self.request.session["currently"] = GroupProfile.BAILLEUR
        self.service = services_programmes.ConventionSelectionService(
            request=self.request
        )

    def test_get_from_db(self):
        bailleurs = Bailleur.objects.filter(siret__in=["987654321", "12345678901234"])
        lots = (
            Lot.objects.filter(programme__bailleur__in=bailleurs)
            .order_by(
                "programme__ville", "programme__nom", "nb_logements", "financement"
            )
            .filter(programme__parent_id__isnull=True)
        )
        self.service.get_from_db()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertIsInstance(self.service.form, ProgrammeSelectionFromDBForm)
        self.assertEqual(
            self.service.form.declared_fields["lot"].choices,
            [(lot.uuid, str(lot)) for lot in lots],
        )

    def test_post_from_db_failed(self):
        self.service.request.POST = {"lot": ""}
        self.service.post_from_db()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("lot"))

        bailleur = Bailleur.objects.get(siret="2345678901")
        administration = Administration.objects.get(code="12345")
        programme = utils_fixtures.create_programme(
            bailleur, administration, nom="Programme failed"
        )
        utils_fixtures.create_lot(programme, Financement.PLAI)
        lot_plus = utils_fixtures.create_lot(programme, Financement.PLUS)
        self.service.request.POST = {"lot": str(lot_plus.uuid)}
        self.service.post_from_db()

        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("lot"))

    def test_post_from_db_success(self):

        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="75000")
        programme_2 = utils_fixtures.create_programme(
            bailleur, administration, nom="Programme 2"
        )
        utils_fixtures.create_lot(programme_2, Financement.PLAI)
        lot_plus_2 = utils_fixtures.create_lot(programme_2, Financement.PLUS)

        self.service.request.POST = {"lot": str(lot_plus_2.uuid)}
        self.service.post_from_db()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.SUCCESS)
        self.assertEqual(
            self.service.convention, Convention.objects.get(lot=lot_plus_2)
        )

    def test_get_from_zero(self):
        administrations = Administration.objects.all().order_by("nom")
        bailleurs = Bailleur.objects.filter(
            siret__in=["987654321", "12345678901234"]
        ).order_by("nom")
        self.service.get_from_zero()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertIsInstance(self.service.form, ProgrammeSelectionFromZeroForm)
        self.assertEqual(
            self.service.form.declared_fields["administration"].choices,
            [
                (administration.uuid, str(administration))
                for administration in administrations
            ],
        )
        self.assertEqual(
            self.service.form.declared_fields["bailleur"].choices,
            [(bailleur.uuid, str(bailleur)) for bailleur in bailleurs],
        )

    def test_post_from_zero_failed_form(self):
        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="75000")
        self.service.request.POST = {
            "bailleur": str(bailleur.uuid),
            "administration": str(administration.uuid),
            "nom": "Programme de test",
            "nb_logements": "10",
            "type_habitat": TypeHabitat.MIXTE,
            "financement": Financement.PLUS,
            "code_postal": "20000",
            "ville": "",
        }
        self.service.post_from_zero()
        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("ville"))

    def test_post_from_zero_failed_scope(self):
        bailleur = Bailleur.objects.get(siret="2345678901")
        administration = Administration.objects.get(code="75000")
        self.service.request.POST = {
            "bailleur": str(bailleur.uuid),
            "administration": str(administration.uuid),
            "nom": "Programme de test",
            "nb_logements": "10",
            "type_habitat": TypeHabitat.MIXTE,
            "financement": Financement.PLUS,
            "code_postal": "20000",
            "ville": "Bisouville",
        }
        self.service.post_from_zero()

        self.assertEqual(self.service.return_status, utils.ReturnStatus.ERROR)
        self.assertTrue(self.service.form.has_error("bailleur"))

    def test_post_from_zero_success(self):
        bailleur = Bailleur.objects.get(siret="987654321")
        administration = Administration.objects.get(code="75000")
        self.service.request.POST = {
            "bailleur": str(bailleur.uuid),
            "administration": str(administration.uuid),
            "nom": "Programme de test",
            "nb_logements": "10",
            "type_habitat": TypeHabitat.MIXTE,
            "financement": Financement.PLUS,
            "code_postal": "20000",
            "ville": "Bisouville",
        }
        self.service.post_from_zero()

        self.assertEqual(self.service.return_status, utils.ReturnStatus.SUCCESS)
        self.assertEqual(
            self.service.convention,
            Convention.objects.get(
                programme__nom="Programme de test", financement=Financement.PLUS
            ),
        )