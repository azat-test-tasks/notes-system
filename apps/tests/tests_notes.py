from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from apps.notes.models import Note


class NoteListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

        self.note1 = Note.objects.create(
            title="Test Note 1",
            description="This is a test note 1.",
            user=self.user,
        )
        self.note2 = Note.objects.create(
            title="Test Note 2",
            description="This is a test note 2.",
            user=self.user,
        )

    def test_get_notes_list_authenticated(self):
        url = reverse("notes-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notes_list_unauthenticated(self):
        url = reverse("notes-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_note_authenticated(self):
        url = reverse("notes-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {"title": "Test Note 3", "description": "This is a test note 3."}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 3)
        self.assertEqual(Note.objects.get(id=3).title, "Test Note 3")

    def test_create_note_unauthenticated(self):
        url = reverse("notes-list")
        data = {"title": "Test Note 3", "description": "This is a test note 3."}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_note_authenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "title": "Test Note 1 Updated",
            "description": "This is a test note 1 updated.",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Note.objects.get(id=self.note1.id).title, "Test Note 1 Updated"
        )

    def test_update_note_unauthenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        data = {
            "title": "Test Note 1 Updated",
            "description": "This is a test note 1 updated.",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_note_unauthorized(self):
        url = reverse("notes-detail", args=[self.note2.id])
        self.client.force_authenticate(user=None)
        data = {
            "title": "Test Note 2 Updated",
            "description": "This is a test note 2 updated.",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_note_authenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 1)

    def test_delete_note_unauthenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoteDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

        self.note1 = Note.objects.create(
            title="Test Note 1",
            description="This is a test note 1.",
            user=self.user,
        )

    def test_get_note_detail_authenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_detail_unauthenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_note_detail_authenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {
            "title": "Test Note 1 Updated",
            "description": "This is a test note 1 updated.",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Note.objects.get(id=self.note1.id).title, "Test Note 1 Updated"
        )

    def test_update_note_detail_unauthenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        data = {
            "title": "Test Note 1 Updated",
            "description": "This is a test note 1 updated.",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_note_detail_authenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

    def test_delete_note_detail_unauthenticated(self):
        url = reverse("notes-detail", args=[self.note1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
