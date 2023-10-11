from django.test import TestCase
from django.urls import reverse

from .models import Letting, Address


class LettingsIndexViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lettings/index.html")
        self.assertContains(response, "<title>Lettings</title>")


class LettingsLettingViewTest(TestCase):
    def test_view_uses_correct_template(self):
        test_address = Address.objects.create(
            number=42,
            street="Meaning Ave",
            city="Universe",
            state="GAL",
            zip_code=12345,
            country_iso_code="UNI",
        )
        test_letting = Letting.objects.create(
            title="Test Letting", address=test_address
        )
        response = self.client.get(
            reverse("lettings:letting", kwargs={"letting_id": test_letting.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lettings/letting.html")
        self.assertContains(response, f"<title>{test_letting.title}</title>")
