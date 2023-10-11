from django.test import TestCase
from django.urls import reverse


class ProfilesIndexViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "<title>Holiday Homes</title>")
