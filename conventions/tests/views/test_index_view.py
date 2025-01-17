from bs4 import BeautifulSoup
from django.http.request import HttpRequest
from django.test import TestCase
from django.urls import reverse

from conventions.services.search import UserConventionSearchService
from conventions.views.conventions import ConventionSearchView, ConventionTabsMixin
from users.models import User


class ConventionIndexViewTests(TestCase):
    fixtures = [
        "auth.json",
        "departements.json",
        "avenant_types.json",
        "bailleurs_for_tests.json",
        "instructeurs_for_tests.json",
        "programmes_for_tests.json",
        "conventions_for_tests.json",
        "users_for_tests.json",
    ]

    def test_get_index(self):
        # login as superuser
        self.client.post(reverse("login"), {"username": "nicolas", "password": "12345"})

        response = self.client.get(reverse("conventions:index"))
        self.assertRedirects(response, reverse("conventions:search_instruction"))

    def test_get_list_active(self):
        """
        Test displaying convention list as superuser without filter nor order
        """
        # login as superuser
        self.client.post(reverse("login"), {"username": "nicolas", "password": "12345"})

        response = self.client.get(reverse("conventions:search_instruction"))
        soup = BeautifulSoup(response.content, "html.parser")
        galion_refs = soup.find_all(attrs={"data-test-role": "programme-galion-cell"})
        financements = soup.find_all(
            attrs={"data-test-role": "programme-financement-cell"}
        )

        self.assertEqual(len(galion_refs), 4)
        self.assertEqual(len(financements), 4)
        self.assertEqual(
            {r.text.strip() for r in galion_refs}, {"Op. : 12345", "Op. : 98765"}
        )
        self.assertEqual({f.text.strip() for f in financements}, {"PLAI", "PLUS"})

    def test_get_list_active_ordered_by_bailleur(self):
        """
        Test displaying convention list as superuser without filter but with bailleur order
        """
        # login as superuser
        self.client.post(reverse("login"), {"username": "nicolas", "password": "12345"})

        response = self.client.get(
            reverse("conventions:search_instruction"),
            data={"order_by": "programme__bailleur__nom"},
        )
        soup = BeautifulSoup(response.content, "html.parser")
        galion_refs = soup.find_all(attrs={"data-test-role": "programme-galion-cell"})
        financements = soup.find_all(
            attrs={"data-test-role": "programme-financement-cell"}
        )

        self.assertEqual(
            {r.text.strip() for r in galion_refs}, {"Op. : 12345", "Op. : 98765"}
        )
        self.assertEqual({f.text.strip() for f in financements}, {"PLUS", "PLAI"})

    def test_get_tabs_basic(self):
        class DummyClassWithTabs(ConventionTabsMixin):
            def __init__(self):
                self.request = HttpRequest()
                self.request.user = User.objects.get(username="nicolas")

        self.assertEqual(len(DummyClassWithTabs().get_tabs()), 3)

    def test_get_tabs_with_new_view(self):
        class DummyClassWithTabs(ConventionTabsMixin):
            def __init__(self):
                self.request = HttpRequest()
                self.request.user = User.objects.get(username="nicolas")

        class DummyService(UserConventionSearchService):
            weight = 1000000
            verbose_name = "Je suis un service"

        class DummyConventionView(ConventionSearchView):
            name = "search_instruction"
            service_class = DummyService

        tabs = DummyClassWithTabs().get_tabs()

        self.assertEqual(len(tabs), 4)
        self.assertEqual(tabs[-1]["title"], "Je suis un service")
