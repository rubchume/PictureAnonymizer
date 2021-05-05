import os
from pathlib import Path
from unittest import mock

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework import status


class UploadPictureTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        if Path(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg")).is_file():
            os.remove(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg"))

        if Path(os.path.join("media/blurred_pictures", "ExamplePictureBlurred.jpg")).is_file():
            os.remove(os.path.join("media/blurred_pictures", "ExamplePictureBlurred.jpg"))

    def test_upload_view_is_up_and_running(self):
        # When
        response = Client().get("/upload_picture/")
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "<title>Upload Picture</title>")

    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_upload_file(self, _):
        # Given
        file1 = File(open('tests/helpers/ExamplePicture.jpg', 'rb'))
        uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file1.read())
        file1.close()

        # When
        response = self.client.post("/upload_picture/", {"picture": uploaded_file}, follow=False)

        # Then
        self.assertRedirects(response, "/upload_picture/?success=True")
        self.assertTrue(Path("media/original_pictures/unique_identifier-asdf.jpg").is_file())
