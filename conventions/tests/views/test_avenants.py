from django.test import TestCase
from django.urls import reverse

from conventions.tests.views.abstract import AbstractCreateViewTestCase
from conventions.models import AvenantType
from bailleurs.models import Bailleur

from conventions.models import Pret

from users.models import User
from unittest.mock import patch


class RemoveFromAvenantViewTest(AbstractCreateViewTestCase, TestCase):
    fixtures = [
        "auth.json",
        "avenant_types.json",
        "bailleurs_for_tests.json",
        "instructeurs_for_tests.json",
        "programmes_for_tests.json",
        "conventions_for_tests.json",
        "users_for_tests.json",
    ]

    def setUp(self):
        super().setUp()
        self.user = User.objects.get(pk=1)
        self.target_path = reverse(
            "conventions:remove_from_avenant", args=[self.convention_75.uuid]
        )
        self.get_expected_http_code = 405
        self.post_success_http_code = 302
        self.post_error_http_code = 302
        self.msg_prefix = "[RemoveFromAvenantViewTest] "
        self.target_template = None
        self.next_target_starts_with = "/conventions/recapitulatif/"

    def test_reset_avenant_type_bailleur(self):
        self._login_as_superuser()

        self.convention_75.signataire_nom = "Obiwan kenobi"
        self.convention_75.save()

        avenant = self.convention_75.clone(
            user=self.user, convention_origin=self.convention_75
        )

        avenant_type_bailleur = AvenantType.objects.get(nom="bailleur")
        avenant.avenant_types.add(avenant_type_bailleur)

        avenant.signataire_nom = "Anakin Skywalker"
        avenant.save()

        bailleur = self.convention_75.programme.bailleur
        autre_bailleur = Bailleur.objects.get(pk=2)
        assert bailleur != autre_bailleur
        avenant.programme.bailleur = autre_bailleur
        avenant.programme.save()

        response = self.client.post(
            reverse("conventions:remove_from_avenant", args=[avenant.uuid]),
            {"avenant_type": avenant_type_bailleur.nom},
        )
        self.assertEqual(
            response.status_code, self.post_success_http_code, msg=f"{self.msg_prefix}"
        )

        avenant.refresh_from_db()
        self.assertEqual(avenant.signataire_nom, "Obiwan kenobi")
        self.assertEqual(avenant.programme.bailleur, bailleur)

    def test_reset_avenant_type_duree(self):
        self._login_as_superuser()

        Pret.objects.create(id=888, convention=self.convention_75, montant=100000)
        Pret.objects.create(id=999, convention=self.convention_75, montant=100001)
        self.assertEqual(self.convention_75.prets.count(), 2)
        self.assertEqual(Pret.objects.count(), 2)

        avenant = self.convention_75.clone(
            user=self.user, convention_origin=self.convention_75
        )

        avenant_type_duree = AvenantType.objects.get(pk=3)
        avenant.avenant_types.add(avenant_type_duree)

        self.assertEqual(self.convention_75.prets.count(), 2)
        self.assertEqual(Pret.objects.count(), 4)
        avenant_pret_ids = list(avenant.prets.values_list("id", flat=True))

        response = self.client.post(
            reverse("conventions:remove_from_avenant", args=[avenant.uuid]),
            {"avenant_type": avenant_type_duree.nom},
        )
        self.assertEqual(
            response.status_code, self.post_success_http_code, msg=f"{self.msg_prefix}"
        )

        self.assertEqual(self.convention_75.prets.count(), 2)
        self.assertEqual(Pret.objects.count(), 4)
        cloned_pret_ids = list(avenant.prets.values_list("id", flat=True))

        self.assertFalse(Pret.objects.filter(pk__in=avenant_pret_ids).exists())
        self.assertTrue(Pret.objects.filter(pk__in=cloned_pret_ids).exists())
        self.assertTrue(Pret.objects.filter(pk__in=(888, 999)).exists())

    def test_no_avenant_type_exist(self):
        self._login_as_superuser()

        avenant = self.convention_75.clone(
            user=self.user, convention_origin=self.convention_75
        )
        self.assertEqual(avenant.avenant_types.count(), 0)

        avenant_type_bailleur = AvenantType.objects.get(nom="bailleur")

        with patch(
            "conventions.signals._update_nested_convention_field"
        ) as mock_update_method:
            response = self.client.post(
                reverse("conventions:remove_from_avenant", args=[avenant.uuid]),
                {"avenant_type": avenant_type_bailleur.nom},
            )

        self.assertEqual(
            response.status_code, self.post_success_http_code, msg=f"{self.msg_prefix}"
        )
        mock_update_method.assert_not_called()

    def test_last_avenant_or_parent(self):
        self._login_as_superuser()

        avenant_type_logements = AvenantType.objects.get(nom="logements")

        self.convention_75.lot.surface_locaux_collectifs_residentiels = 12.0
        self.convention_75.lot.surface_habitable_totale = 50.0
        self.convention_75.lot.save()

        avenant_1 = self.convention_75.clone(
            user=self.user, convention_origin=self.convention_75
        )
        avenant_1.lot.surface_locaux_collectifs_residentiels = 15.0
        avenant_1.lot.save()
        avenant_1.avenant_types.add(avenant_type_logements)

        avenant_2 = avenant_1.clone(
            user=self.user, convention_origin=self.convention_75
        )
        avenant_2.lot.surface_habitable_totale = 60.0
        avenant_2.lot.save()
        avenant_2.avenant_types.add(avenant_type_logements)

        avenant_3 = avenant_2.clone(
            user=self.user, convention_origin=self.convention_75
        )
        avenant_3.lot.surface_locaux_collectifs_residentiels = 30.0
        avenant_3.lot.surface_habitable_totale = 70.0
        avenant_3.lot.save()
        avenant_3.avenant_types.add(avenant_type_logements)

        response = self.client.post(
            reverse("conventions:remove_from_avenant", args=[avenant_3.uuid]),
            {"avenant_type": avenant_type_logements.nom},
        )
        self.assertEqual(
            response.status_code, self.post_success_http_code, msg=f"{self.msg_prefix}"
        )

        avenant_3.refresh_from_db()
        self.assertEqual(avenant_3.lot.surface_locaux_collectifs_residentiels, 15.0)
        self.assertEqual(avenant_3.lot.surface_habitable_totale, 60.0)
