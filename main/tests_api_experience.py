import uuid

from django.contrib.auth.models import Group, User
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):
    def setUp(self):
        Experience.objects.all().delete()
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.visitor = User.objects.create_user(username="visitor", password="test-password")

        self.experience = Experience.objects.create(
            title="Asisten Dosen", description="Membantu mahasiswa.",
            category="committee", role="Asisten Dosen", started_at="2026-01-01",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Data Analyst Intern", "description": "Membuat dashboard.",
            "category": "internship", "thumbnail": "",
            "started_at": "2026-02-01", "ended_at": "2026-06-01",
            "role": "Intern", "is_featured": False, "display_order": 1,
        }

    # Read
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = response.data[0]
        self.assertEqual(item["id"], str(self.experience.id))
        self.assertEqual(item["category_display"], "Committee")
        self.assertTrue(item["is_ongoing"])
        self.assertFalse(item["is_starred"])
        self.assertNotIn("fields", item)
        self.assertNotIn("email", str(response.content))
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_filter_sort_and_empty(self):
        other = Experience.objects.create(
            title="Magang", description="x", category="internship",
            role="Analyst", started_at="2025-01-01",
        )
        other.starred_by.add(self.visitor)

        by_title = self.client.get(self.list_url, {"title": "Asisten"})
        self.assertEqual(len(by_title.data), 1)
        by_role = self.client.get(self.list_url, {"title": "analyst"})
        self.assertEqual(by_role.data[0]["id"], str(other.id))
        by_category = self.client.get(self.list_url, {"category": "internship"})
        self.assertEqual([i["id"] for i in by_category.data], [str(other.id)])

        default_order = self.client.get(self.list_url)
        self.assertEqual(default_order.data[0]["id"], str(self.experience.id))
        by_stars = self.client.get(self.list_url, {"sort": "stars"})
        self.assertEqual(by_stars.data[0]["id"], str(other.id))

        self.assertEqual(self.client.get(self.list_url, {"title": "tidak-ada"}).data, [])

    def test_list_query_count_does_not_grow_with_rows(self):
        """Prefetch starred_by mencegah query tambahan per baris (N+1)."""
        with CaptureQueriesContext(connection) as one_row:
            self.client.get(self.list_url)

        for index in range(5):
            experience = Experience.objects.create(
                title=f"Pengalaman {index}", description="x", role="Peran",
                started_at="2025-01-01",
            )
            experience.starred_by.add(self.owner, self.editor, self.visitor)

        with CaptureQueriesContext(connection) as six_rows:
            response = self.client.get(self.list_url)

        self.assertEqual(len(response.data), 6)
        self.assertEqual(len(six_rows), len(one_row))
        # Satu query untuk daftar + satu query prefetch pemberi star.
        self.assertEqual(len(six_rows), 2)

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    # Permissions
    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen")

    def test_denial_message_explains_the_rule(self):
        self.client.force_authenticate(user=self.visitor)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("pemilik", str(response.data["detail"]))

    def test_editor_can_patch_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Edited"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_staff_without_editor_group_cannot_write(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen")

    def test_regular_user_can_read_and_star_only(self):
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.options(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)

    # Owner actions
    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.description, "Membantu mahasiswa.")

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Validation
    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"description": "<b></b>"}, "description"),
            ({"role": "<i></i>"}, "role"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"category": "tidak-ada"}, "category"),
            ({"ended_at": "2025-01-01"}, "ended_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_text_is_stripped_of_tags(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url, {**self.payload, "title": "<b>Magang</b> Data"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Magang Data")

    def test_patch_date_validation_uses_existing_values(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"ended_at": "2025-12-31"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", response.data)
        self.experience.refresh_from_db()
        self.assertIsNone(self.experience.ended_at)

    # Star
    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], "visitor")
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "is_ongoing": True,
            "category_display": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        self.assertFalse(response.data["is_ongoing"])
        self.assertEqual(response.data["category_display"], "Internship")

    # CSRF
    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)