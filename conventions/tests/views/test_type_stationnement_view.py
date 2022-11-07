from django.test import TestCase
from django.urls import reverse

from conventions.tests.views.abstract import AbstractViewTestCase


class ConventionTypeStationnementViewTests(AbstractViewTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.target_path = reverse(
            "conventions:stationnements", args=[self.convention_75.uuid]
        )
        self.next_target_path = reverse(
            "conventions:comments", args=[self.convention_75.uuid]
        )
        self.target_template = "conventions/stationnements.html"
        self.error_payload = {
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
        self.success_payload = {
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
        self.msg_prefix = "[ConventionTypeStationnementViewTests] "