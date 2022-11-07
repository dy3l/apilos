from django.test import TestCase
from django.urls import reverse

from conventions.tests.views.abstract import AbstractViewTestCase


class ConventionCommentsViewTests(AbstractViewTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.target_path = reverse(
            "conventions:comments", args=[self.convention_75.uuid]
        )
        self.next_target_path = reverse(
            "conventions:recapitulatif", args=[self.convention_75.uuid]
        )
        self.target_template = "conventions/comments.html"
        self.error_payload = {"comments": "O" * 5001}
        self.success_payload = {"comments": "This is a comment"}
        self.msg_prefix = "[ConventionCommentsViewTests] "

    def _test_data_integrity(self):
        self.convention_75.refresh_from_db()
        self.assertEqual(
            self.convention_75.comments,
            '{"files": [], "text": "This is a comment"}',
            msg=f"{self.msg_prefix}",
        )


class AvenantCommentsViewTests(ConventionCommentsViewTests):
    def setUp(self):
        super().setUp()
        self.target_path = reverse(
            "conventions:avenant_comments", args=[self.convention_75.uuid]
        )
        self.next_target_path = reverse(
            "conventions:recapitulatif", args=[self.convention_75.uuid]
        )
        self.msg_prefix = "[AvenantCommentsViewTests] "