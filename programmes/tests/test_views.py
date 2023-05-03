import re

from django.http import HttpResponseBadRequest
from django.test import TestCase, override_settings
from django.urls import reverse
import responses


def _cerbere_request(request):
    print("OUUUIIIIIII")
    print(request)
    return HttpResponseBadRequest("Oh mais hey!")


# @override_settings(USE_MOCKED_SIAP_CLIENT=True)
@override_settings(CERBERE_AUTH="https://cerbere.com")
class OperationConventionViewTests(TestCase):
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

    @responses.activate
    # @override_settings(CAS_SESSION_FACTORY=None)
    def test_create_operation(self):
        responses.add_callback(
            responses.POST,
            re.compile("http://test.apilos.beta.gouv.fr/cas/test/.*"),
            _cerbere_request,
        )
        responses.add_callback(
            responses.GET,
            re.compile("http://test.apilos.beta.gouv.fr/cas/test/.*"),
            _cerbere_request,
        )
        route = reverse("programmes:operation_conventions", args=["2021CG0330012"])

        response = self.client.get(f"/accounts/cerbere-login?TICKET=josiane@apilos.com")
        print(response)

        # self.assertRedirects(response, "http://test.apilos.beta.gouv.fr/cas/test/")

        # self.client.post("http://test.apilos.beta.gouv.fr/cas/test/", {
        #     'login': "josiane@apilos.com",
        #     'password': "solipa",
        # })

        # response = self.client.get(
        #     reverse("programmes:operation_conventions", args=['2021CG0330012']),
        #     data={
        #         'habilitation_id': 2592
        #     }
        # )
        #
        # self.assertEqual(200, response.status_code)
