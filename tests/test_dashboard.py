import os
from pathlib import Path
from unittest import mock

from bs4 import BeautifulSoup
from core.models import Picture
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework import status


class DashboardTests(TestCase):
    def tearDown(self):
        if Path(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg")).is_file():
            os.remove(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg"))

        if Path(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg")).is_file():
            os.remove(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg"))

        if Path(os.path.join("media/original_pictures", "another_identifier.jpg")).is_file():
            os.remove(os.path.join("media/original_pictures", "another_identifier.jpg"))

        if Path(os.path.join("media/blurred_pictures", "another_identifier.jpg")).is_file():
            os.remove(os.path.join("media/blurred_pictures", "another_identifier.jpg"))

    def test_dashboard_view_is_up_and_running(self):
        # When
        response = Client().get("/dashboard/")
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "<title>Dashboard</title>")

    def test_show_no_images_if_no_image_is_saved(self):
        # When
        response = Client().get("/dashboard/")
        # Then
        self.assertNotContains(response, "<img>")

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_show_one_image(self, _, blurred_image):
        # Given
        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as image_file:
            Picture(
                picture=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                ),
            ).save()
        # When
        response = Client().get("/dashboard/")
        # Then
        self.assertContains(
            response,
            '<img src="/media/blurred_pictures/unique_identifier-asdf.jpg" alt="img">'
        )

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4")
    def test_show_multiple_images(self, uuid4, blurred_image):
        # Given
        uuid4.side_effect = [
            "unique_identifier-asdf",
            "another_identifier"
        ]

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as image_file:
            Picture(
                picture=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                ),
            ).save()

            Picture(
                picture=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                ),
            ).save()
        # When
        response = Client().get("/dashboard/")
        # Then
        self.assertContains(
            response,
            '<img src="/media/blurred_pictures/unique_identifier-asdf.jpg" alt="img">'
        )
        self.assertContains(
            response,
            '<img src="/media/blurred_pictures/another_identifier.jpg" alt="img">'
        )

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4")
    def test_do_not_show_image_if_there_is_no_file_associated_with_it(self, uuid4, blurred_image):
        # Given
        uuid4.side_effect = [
            "unique_identifier-asdf",
            "another_identifier"
        ]

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as image_file:
            Picture(
                picture=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                ),
            ).save()

            p = Picture(
                picture=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                ),
            )

            p.save()
            p.picture_blurred = None
            p.save()
        # When
        response = Client().get("/dashboard/")
        # Then
        self.assertContains(
            response,
            '<img src="/media/blurred_pictures/unique_identifier-asdf.jpg" alt="img">'
        )
        self.assertNotContains(
            response,
            '<img src="/media/blurred_pictures/another_identifier.jpg" alt="img">'
        )

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4")
    def test_show_multiple_images_in_inverse_order_of_upload(self, uuid4, blurred_image):
        # Given
        uuid4.side_effect = [
            "unique_identifier-asdf",
            "another_identifier"
        ]

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as image_file:
            Picture(
                picture=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                ),
            ).save()

            Picture(
                picture=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=image_file.read(),
                    content_type='image/jpeg'
                ),
            ).save()
        # When
        response = Client().get("/dashboard/")
        # Then
        soup = BeautifulSoup(response.content, "html.parser")
        images = soup.find_all("img")
        self.assertEqual(
            "/media/blurred_pictures/another_identifier.jpg",
            images[0]["src"]
        )
        self.assertEqual(
            "/media/blurred_pictures/unique_identifier-asdf.jpg",
            images[1]["src"]
        )
