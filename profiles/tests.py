from django.test import TestCase
from django.urls import reverse

from .models import Profile
from django.contrib.auth.models import User


class ProfilesIndexViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("profiles:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/index.html")
        self.assertContains(response, "<title>Profiles</title>")


class ProfilesProfileViewTest(TestCase):
    def test_view_uses_correct_template(self):
        test_user = User.objects.create(username="test_user")
        Profile.objects.create(user=test_user, favorite_city="Twin Peaks, Washington")
        response = self.client.get(
            reverse("profiles:profile", kwargs={"username": test_user.username})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertContains(response, f"<title>{test_user.username}</title>")
