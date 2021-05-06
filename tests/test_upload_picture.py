import os
from pathlib import Path
from unittest import mock

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework import status


class UploadPictureTests(TestCase):
    def tearDown(self):
        if Path(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg")).is_file():
            os.remove(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg"))

        if Path(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg")).is_file():
            os.remove(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg"))

    def test_upload_view_is_up_and_running(self):
        # When
        response = Client().get("/upload_picture/")
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "<title>Upload Picture</title>")

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_upload_file(self, _, blurred_image):
        # Given
        file1 = File(open('tests/helpers/ExamplePicture.jpg', 'rb'))
        uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file1.read())
        file1.close()

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        # When
        response = Client().post("/upload_picture/", {"picture": uploaded_file}, follow=False)

        # Then
        self.assertRedirects(response, "/upload_picture/?success=True")
        self.assertTrue(Path("media/original_pictures/unique_identifier-asdf.jpg").is_file())
