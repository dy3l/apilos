import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

import jinja2
from django.conf import settings
from django.test import TestCase

from bailleurs.models import SousNatureBailleur
from conventions.models import Convention, ConventionType1and2
from conventions.services.convention_generator import (
    ConventionTypeConfigurationError,
    _compute_liste_des_annexes,
    _compute_total_logement,
    _get_adresse,
    _get_jinja_env,
    _get_loyer_par_metre_carre,
    _to_fr_float,
    compute_mixte,
    default_str_if_none,
    generate_convention_doc,
    get_convention_template_path,
    pluralize,
    to_fr_date,
    to_fr_date_or_default,
    to_fr_short_date,
    to_fr_short_date_or_default,
    typologie_label,
)
from programmes.models import ActiveNatureLogement, Logement, TypologieLogement
from programmes.models.choices import NatureLogement
from users.models import User


def convention_context_keys():
    return {
        "annexes",
        "res_sh_totale",
        "references_cadastrales",
        "administration",
        "prets_cdc",
        "stationnements",
        "lc_sh_totale",
        "su_totale",
        "lot",
        "programme",
        "liste_des_annexes",
        "mixPLUSinf10_10pc",
        "logements",
        "mixPLUSinf10_30pc",
        "nombre_annees_conventionnement",
        "mixPLUSsup10_30pc",
        "sar_totale",
        "logement_edds",
        "lot_num",
        "mixPLUS_30pc",
        "convention",
        "sh_totale",
        "sa_totale",
        "nb_logements_par_type",
        "locaux_collectifs",
        "loyer_m2",
        "bailleur",
        "mixPLUS_10pc",
        "autres_prets",
        "vendeur_images",
        "effet_relatif_images",
        "adresse",
        "reference_publication_acte_images",
        "code_postal",
        "ville",
        "reference_notaire_images",
        "edd_classique_images",
        "loyer_total",
        "edd_stationnements_images",
        "reference_cadastrale_images",
        "acquereur_images",
        "edd_volumetrique_images",
    }


class ConventionGeneratorComputeMixiteTest(TestCase):
    fixtures = [
        "auth.json",
        "bailleurs_for_tests.json",
        "instructeurs_for_tests.json",
        "programmes_for_tests.json",
        "conventions_for_tests.json",
    ]

    def test_compute_mixite_lt_10(self):
        convention = Convention.objects.get(numero="0001")
        convention.lot.nb_logements = 9
        convention.lot.save()
        self.assertEqual(
            compute_mixte(convention),
            {
                "mixPLUS_10pc": 1,
                "mixPLUS_30pc": 3,
                "mixPLUSinf10_10pc": 1,
                "mixPLUSinf10_30pc": 3,
                "mixPLUSsup10_30pc": 0,
            },
        )
        convention.lot.nb_logements = 5
        convention.lot.save()
        self.assertEqual(
            compute_mixte(convention),
            {
                "mixPLUS_10pc": 1,
                "mixPLUS_30pc": 2,
                "mixPLUSinf10_10pc": 1,
                "mixPLUSinf10_30pc": 2,
                "mixPLUSsup10_30pc": 0,
            },
        )
        convention.lot.nb_logements = 4
        convention.lot.save()
        self.assertEqual(
            compute_mixte(convention),
            {
                "mixPLUS_10pc": 0,
                "mixPLUS_30pc": 1,
                "mixPLUSinf10_10pc": 0,
                "mixPLUSinf10_30pc": 1,
                "mixPLUSsup10_30pc": 0,
            },
        )

    def test_compute_mixite_gt_10(self):
        convention = Convention.objects.get(numero="0001")
        convention.lot.nb_logements = 10
        convention.lot.save()
        self.assertEqual(
            compute_mixte(convention),
            {
                "mixPLUS_10pc": 1,
                "mixPLUS_30pc": 3,
                "mixPLUSinf10_10pc": 0,
                "mixPLUSinf10_30pc": 0,
                "mixPLUSsup10_30pc": 3,
            },
        )
        convention.lot.nb_logements = 11
        convention.lot.save()
        self.assertEqual(
            compute_mixte(convention),
            {
                "mixPLUS_10pc": 1,
                "mixPLUS_30pc": 4,
                "mixPLUSinf10_10pc": 0,
                "mixPLUSinf10_30pc": 0,
                "mixPLUSsup10_30pc": 4,
            },
        )


class ConventionServiceGeneratorTest(TestCase):
    fixtures = [
        "auth.json",
        # "departements.json",
        "avenant_types.json",
        "bailleurs_for_tests.json",
        "instructeurs_for_tests.json",
        "programmes_for_tests.json",
        "conventions_for_tests.json",
        "users_for_tests.json",
    ]

    def test_compute_total_logement(self):
        convention = Convention.objects.get(numero="0001")
        Logement.objects.create(lot=convention.lot, typologie=TypologieLogement.T2)
        Logement.objects.create(lot=convention.lot, loyer=500)

        Logement.objects.create(lot=convention.lot, loyer=1000)

        logements_totale, nb_logements_par_type = _compute_total_logement(convention)
        assert logements_totale == {
            "loyer_total": Decimal("1500.00"),
            "sa_totale": 0,
            "sar_totale": 0,
            "sh_totale": 0,
            "su_totale": 0,
        }
        assert nb_logements_par_type == {"T1": 2, "T2": 1}

    def test_get_adresse(self):
        convention = Convention.objects.get(numero="0001")
        convention.programme.adresse = "22 rue segur"
        convention.programme.code_postal = "75000"
        convention.programme.ville = "Paris"
        convention.adresse = "23 rue segur"

        result = _get_adresse(convention)

        assert result == {
            "adresse": "23 rue segur",
            "code_postal": "75000",
            "ville": "Paris",
        }

    def test_generate_convention_doc(self):
        convention = Convention.objects.get(numero="0001")
        convention.programme.nature_logement = NatureLogement.RESISDENCESOCIALE

        with patch(
            "conventions.services.convention_generator.DocxTemplate.render"
        ) as mocked_render:
            generate_convention_doc(convention)

            args, _ = mocked_render.call_args
            context = args[0]

            mocked_render.assert_called_once()
            assert set(context.keys()) == convention_context_keys()

    def test_get_convention_template_path(self):
        user = User.objects.get(username="fix")
        convention = Convention.objects.get(numero="0001")
        avenant = convention.clone(user, convention_origin=convention)
        self.assertEqual(
            get_convention_template_path(avenant),
            f"{settings.BASE_DIR}/documents/Avenant-template.docx",
        )
        avenant.delete()
        convention.programme.nature_logement = ActiveNatureLogement.AUTRE
        self.assertEqual(
            get_convention_template_path(convention),
            f"{settings.BASE_DIR}/documents/Foyer-template.docx",
        )
        foyer_avenant = convention.clone(user, convention_origin=convention)
        self.assertEqual(
            get_convention_template_path(foyer_avenant),
            f"{settings.BASE_DIR}/documents/FoyerResidence-Avenant-template.docx",
        )

        for nature_logement in [
            ActiveNatureLogement.HEBERGEMENT,
            ActiveNatureLogement.RESIDENCEDACCUEIL,
            ActiveNatureLogement.PENSIONSDEFAMILLE,
            ActiveNatureLogement.RESISDENCESOCIALE,
        ]:
            convention.programme.nature_logement = nature_logement
            self.assertEqual(
                get_convention_template_path(convention),
                f"{settings.BASE_DIR}/documents/Residence-template.docx",
            )
        with self.assertRaises(ConventionTypeConfigurationError):
            convention.programme.nature_logement = (
                ActiveNatureLogement.LOGEMENTSORDINAIRES
            )
            get_convention_template_path(convention)

        convention.programme.nature_logement = ActiveNatureLogement.LOGEMENTSORDINAIRES
        convention.programme.bailleur.sous_nature_bailleur = SousNatureBailleur.SEM_EPL
        convention.programme.bailleur.save()
        self.assertEqual(
            get_convention_template_path(convention),
            f"{settings.BASE_DIR}/documents/SEM-template.docx",
        )

        for sous_nature in [
            SousNatureBailleur.OFFICE_PUBLIC_HLM,
            SousNatureBailleur.SA_HLM_ESH,
            SousNatureBailleur.COOPERATIVE_HLM_SCIC,
        ]:
            convention.programme.bailleur.sous_nature_bailleur = sous_nature
            convention.programme.bailleur.save()
            self.assertEqual(
                get_convention_template_path(convention),
                f"{settings.BASE_DIR}/documents/HLM-template.docx",
            )

        for sous_nature in [
            SousNatureBailleur.ASSOCIATIONS,
        ]:
            convention.programme.bailleur.sous_nature_bailleur = sous_nature
            convention.programme.bailleur.save()
            convention.type1and2 = ConventionType1and2.TYPE1
            self.assertEqual(
                get_convention_template_path(convention),
                f"{settings.BASE_DIR}/documents/Type1-template.docx",
            )
            convention.type1and2 = ConventionType1and2.TYPE2
            self.assertEqual(
                get_convention_template_path(convention),
                f"{settings.BASE_DIR}/documents/Type2-template.docx",
            )
            convention.type1and2 = None
            self.assertRaises(
                ConventionTypeConfigurationError,
                get_convention_template_path,
                convention,
            )

    def test_typologie_label(self):
        self.assertEqual(typologie_label(TypologieLogement.T1.label), "Logement T 1")
        self.assertEqual(
            typologie_label(TypologieLogement.T1prime.label), "Logement T 1'"
        )
        self.assertEqual(typologie_label(TypologieLogement.T7.label), "Logement T 7")
        self.assertEqual(typologie_label(TypologieLogement.T1.value), "Logement T 1")
        self.assertEqual(
            typologie_label(TypologieLogement.T1prime.value), "Logement T 1'"
        )
        self.assertEqual(typologie_label(TypologieLogement.T7.value), "Logement T 7")
        self.assertEqual(typologie_label("Invalid value"), None)

    def test_default_str_if_none(self):
        self.assertEqual(default_str_if_none(None), "---")
        self.assertEqual(default_str_if_none(""), "---")
        self.assertEqual(default_str_if_none("None"), "None")

    def test_to_fr_date(self):
        self.assertEqual(to_fr_date(None), "")
        self.assertEqual(to_fr_date(""), "")
        self.assertEqual(to_fr_date(date(2022, 12, 31)), "31 décembre 2022")

    def test_to_fr_date_or_default(self):
        self.assertEqual(to_fr_date_or_default(None), "---")
        self.assertEqual(to_fr_date_or_default(""), "---")
        self.assertEqual(to_fr_date_or_default(date(2022, 12, 31)), "31 décembre 2022")

    def test_to_fr_short_date(self):
        self.assertEqual(to_fr_short_date(None), "")
        self.assertEqual(to_fr_short_date(""), "")
        self.assertEqual(to_fr_short_date(date(2022, 12, 31)), "31/12/2022")

    def test_to_fr_short_date_or_default(self):
        self.assertEqual(to_fr_short_date_or_default(None), "---")
        self.assertEqual(to_fr_short_date_or_default(""), "---")
        self.assertEqual(to_fr_short_date_or_default(date(2022, 12, 31)), "31/12/2022")

    def test_jinja_env_setup(self):
        jinja_env = _get_jinja_env()

        self.assertIsInstance(jinja_env, jinja2.Environment)
        self.assertTrue(jinja_env.autoescape)

        expected_filters = [
            "d",
            "dd",
            "sd",
            "sdd",
            "f",
            "pl",
            "len",
            "inline_text_multiline",
            "get_text_as_list",
            "default_str_if_none",
            "default_empty_if_none",
            "tl",
        ]

        for filter_name in expected_filters:
            self.assertIn(filter_name, jinja_env.filters)


class TestToFrFloat(unittest.TestCase):
    def test_to_fr_float(self):
        self.assertEqual(_to_fr_float(1234.5678), "1 234,57")
        self.assertEqual(_to_fr_float(1234.5678, 3), "1 234,568")
        self.assertEqual(_to_fr_float(1234.5), "1 234,50")
        self.assertEqual(_to_fr_float(None), "")


class TestPluralize(unittest.TestCase):
    def test_pluralize(self):
        self.assertEqual(pluralize(2), "s")
        self.assertEqual(pluralize(1), "")
        self.assertEqual(pluralize(0), "")
        self.assertEqual(pluralize(None), "")


class TestGetLoyerParMetreCarre(unittest.TestCase):
    def test_get_loyer_par_metre_carre(self):
        # Set up mock objects
        mock_convention = Mock()
        mock_logement = Mock()
        mock_logement.loyer_par_metre_carre = 10.5
        mock_convention.lot.logements.first.return_value = mock_logement

        # Call the function to test
        loyer_par_metre_carre = _get_loyer_par_metre_carre(mock_convention)

        # Check that loyer_par_metre_carre is correct
        self.assertEqual(loyer_par_metre_carre, 10.5)

    def test_get_loyer_par_metre_carre_no_logement(self):
        # Set up mock objects
        mock_convention = Mock()
        mock_convention.lot.logements.first.return_value = None

        # Call the function to test
        loyer_par_metre_carre = _get_loyer_par_metre_carre(mock_convention)

        # Check that loyer_par_metre_carre is correct
        self.assertEqual(loyer_par_metre_carre, 0)


class TestComputeListeDesAnnexes(unittest.TestCase):
    def test_compute_liste_des_annexes(self):
        # Set up mock objects
        mock_annexe1 = Mock()
        mock_annexe1.get_typologie_display.return_value = "Type1"
        mock_annexe2 = Mock()
        mock_annexe2.get_typologie_display.return_value = "Type2"
        mock_annexe3 = Mock()
        mock_annexe3.get_typologie_display.return_value = "Type2"

        mock_stationnement1 = Mock()
        mock_stationnement1.get_typologie_display.return_value = "Type1"
        mock_stationnement1.nb_stationnements = 1
        mock_stationnement2 = Mock()
        mock_stationnement2.get_typologie_display.return_value = "Type2"
        mock_stationnement2.nb_stationnements = 3

        annexes = [mock_annexe1, mock_annexe2, mock_annexe3]
        typestationnements = [mock_stationnement1, mock_stationnement2]

        # Call the function to test
        annexes_list = _compute_liste_des_annexes(typestationnements, annexes)

        # Check that annexes_list is correct
        expected_annexes_list = (
            "1 annexe de type type1,"
            " 2 annexes de type type2,"
            " 1 stationnement de type type1,"
            " 3 stationnements de type type2"
        )
        self.assertEqual(annexes_list, expected_annexes_list)
