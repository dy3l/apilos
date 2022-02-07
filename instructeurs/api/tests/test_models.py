from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import utils_fixtures
from users.models import User, Role
from users.type_models import TypeRole
from instructeurs.models import Administration

ADMINISTRATION_READ_FIELDS = ["uuid", "nom", "code", "ville_signature"]


class SuperUserAPITest(APITestCase):
    """
    As super user, I can do anything using the API
    """

    def setUp(self):
        User.objects.create_superuser("nico_administration", "nico@apilos.com", "12345")
        self.client.login(username="nico_administration", password="12345")
        (
            self.administration_arles,
            self.administration_marseille,
        ) = utils_fixtures.create_administrations()

    def test_can_get_administration_list(self):
        response = self.client.get("/api/v1/administrations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_can_get_administration(self):
        response = self.client.get(
            f"/api/v1/administrations/{self.administration_arles.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ADMINISTRATION_READ_FIELDS)

    def test_can_create_administration(self):
        response = self.client.post(
            "/api/v1/administrations/",
            {"nom": "ddtm", "code": "54321", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(list(response.data.keys()), ADMINISTRATION_READ_FIELDS)

    def test_can_update_administration(self):
        response = self.client.put(
            f"/api/v1/administrations/{self.administration_arles.uuid}/",
            {"nom": "ddtm 2", "code": "65432", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ADMINISTRATION_READ_FIELDS)
        self.assertEqual(
            dict(response.data),
            {
                "uuid": f"{self.administration_arles.uuid}",
                "nom": "ddtm 2",
                "code": "65432",
                "ville_signature": "paris",
            },
        )

    def test_can_delete_administration(self):
        response = self.client.delete(
            f"/api/v1/administrations/{self.administration_arles.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            list(Administration.objects.filter(uuid=self.administration_arles.uuid)), []
        )


class InstructeurUserAPITest(APITestCase):
    """
    As instructeur, I am able to :
    * Read any Administration
    * Update administration in my current scope
    * I don't have right to remove or create any administration
    """

    def setUp(self):
        user_instructeur = User.objects.create_user(
            "sabine_administration", "sabine@apilos.com", "12345"
        )
        self.client.login(username="sabine_administration", password="12345")
        (
            self.administration_arles,
            self.administration_marseille,
        ) = utils_fixtures.create_administrations()
        group_instructeur = utils_fixtures.create_group(
            "Instructeur", ru=["administration"]
        )
        Role.objects.create(
            typologie=TypeRole.INSTRUCTEUR,
            administration=self.administration_arles,
            user=user_instructeur,
            group=group_instructeur,
        )

    def test_can_get_administration_list(self):
        # As instructeur I can list any administration
        response = self.client.get("/api/v1/administrations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_can_get_administration(self):
        # As instructeur I can get any administration that I own
        response = self.client.get(
            f"/api/v1/administrations/{self.administration_arles.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ADMINISTRATION_READ_FIELDS)
        # and that I don't own
        response = self.client.get(
            f"/api/v1/administrations/{self.administration_marseille.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ADMINISTRATION_READ_FIELDS)

    def test_can_create_administration(self):
        # As instructeur I don't have right to create administration
        response = self.client.post(
            "/api/v1/administrations/",
            {"nom": "ddtm", "code": "54321", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_administration(self):
        # As instructeur I have right to update administration that I own
        response = self.client.put(
            f"/api/v1/administrations/{self.administration_arles.uuid}/",
            {"nom": "ddtm 2", "code": "65432", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            dict(response.data),
            {
                "uuid": f"{self.administration_arles.uuid}",
                "nom": "ddtm 2",
                "code": "65432",
                "ville_signature": "paris",
            },
        )
        # As instructeur I don't have right to update administration that I don't own
        response = self.client.put(
            f"/api/v1/administrations/{self.administration_marseille.uuid}/",
            {"nom": "ddtm 2", "code": "65432", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_administration(self):
        # As instructeur I don't have right to remove administration that I own
        response = self.client.delete(
            f"/api/v1/administrations/{self.administration_arles.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # neither administration that I don't own
        response = self.client.delete(
            f"/api/v1/administrations/{self.administration_marseille.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BailleurUserAPITest(APITestCase):
    """
    As bailleur, I am able to :
    * Read any Administration
    * I don't have right to remove, create or update any administration
    """

    def setUp(self):
        user_bailleur = User.objects.create_user(
            "raph_administration", "raph@apilos.com", "12345"
        )
        self.client.login(username="raph_administration", password="12345")
        (
            self.administration_arles,
            self.administration_marseille,
        ) = utils_fixtures.create_administrations()
        group_bailleur = utils_fixtures.create_group("Bailleur", ro=["administration"])
        bailleur = utils_fixtures.create_bailleur()
        Role.objects.create(
            typologie=TypeRole.BAILLEUR,
            bailleur=bailleur,
            user=user_bailleur,
            group=group_bailleur,
        )

    def test_can_get_administration_list(self):
        # As bailleur I can list any administration
        response = self.client.get("/api/v1/administrations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_can_get_administration(self):
        # As bailleur I can get any administration that I own
        response = self.client.get(
            f"/api/v1/administrations/{self.administration_arles.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ADMINISTRATION_READ_FIELDS)
        # and that I don't own
        response = self.client.get(
            f"/api/v1/administrations/{self.administration_marseille.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ADMINISTRATION_READ_FIELDS)

    def test_can_create_administration(self):
        # As bailleur I don't have right to create administration
        response = self.client.post(
            "/api/v1/administrations/",
            {"nom": "ddtm", "code": "54321", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_administration(self):
        # As bailleur I don't have right to update administration that I own
        response = self.client.put(
            f"/api/v1/administrations/{self.administration_arles.uuid}/",
            {"nom": "ddtm 2", "code": "65432", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # neither administration that I don't own
        response = self.client.put(
            f"/api/v1/administrations/{self.administration_marseille.uuid}/",
            {"nom": "ddtm 2", "code": "65432", "ville_signature": "paris"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_administration(self):
        # As bailleur I don't have right to remove administration that I own
        response = self.client.delete(
            f"/api/v1/administrations/{self.administration_arles.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # neither administration that I don't own
        response = self.client.delete(
            f"/api/v1/administrations/{self.administration_marseille.uuid}/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)