from django.test import TestCase
from django.urls import reverse


class LettingIndexViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lettings/index.html")

    def test_mytest(self):
        self.assertTrue(True)
