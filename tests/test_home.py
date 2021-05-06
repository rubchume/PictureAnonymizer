from django.test import Client, TestCase
from django.urls import reverse


class HomeTests(TestCase):
    def test_home_redirects_to_upload_page(self):
        response = Client().get("/")
        # Then
        self.assertRedirects(
            response,
            reverse("upload_picture"),
            status_code=302,
            target_status_code=200,
        )
