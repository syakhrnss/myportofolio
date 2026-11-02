from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        Experience.objects.all().delete()
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="committee",
            role="Asisten Dosen",
            started_at=timezone.localdate(),
        )


    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "committee")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, "Committee")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        api_response = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(api_response.status_code, 200)
        item = next(
            i for i in api_response.json() if i["pk"] == str(self.experience.id)
        )
        fields = item["fields"]
        self.assertEqual(fields["title"], self.experience.title)
        self.assertEqual(fields["description"], self.experience.description)
        self.assertEqual(fields["category_display"], "Committee")
        self.assertTrue(fields["is_ongoing"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response, "Belum ada pengalaman yang ditambahkan atau ditemukan."
        )
        api_response = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(api_response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.localdate()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

        api_response = self.client.get(reverse("main:get_experiences_json"))
        item = next(
            i for i in api_response.json() if i["pk"] == str(self.experience.id)
        )
        self.assertFalse(item["fields"]["is_ongoing"])

    def test_projects_page(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_data_appears(self):
        project = Project.objects.create(
            title="Test Project",
            subtitle="Personal Project",
            image="img/project1.png",
            description="Ini testt.",
        )

        response = self.client.get(reverse("api:project-list"))
        self.assertEqual(response.status_code, 200)

        item = next(i for i in response.json() if i["id"] == project.id)
        self.assertEqual(item["title"], project.title)
        self.assertEqual(item["subtitle"], project.subtitle)
        self.assertEqual(item["description"], project.description)

    def test_empty_project_page(self):
        Project.objects.all().delete()

        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Belum ada proyek yang ditambahkan atau ditemukan.",
        )

        api_response = self.client.get(reverse("api:project-list"))
        self.assertEqual(api_response.json(), [])