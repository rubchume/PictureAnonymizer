import io
import os
from pathlib import Path
import unittest
from unittest import mock

from core.models import Picture
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import numpy as np
import pytest
from skimage.io import imread


@pytest.mark.django_db
class PictureModelTests(unittest.TestCase):
    def tearDown(self):
        if Path(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg")).is_file():
            os.remove(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg"))

        if Path(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg")).is_file():
            os.remove(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg"))

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_create_unique_id_when_saving_model_instance(self, _, blurred_image):
        # Given
        with open('tests/helpers/ExamplePicture.jpg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file.read())

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        picture = Picture(picture=uploaded_file)
        # When
        picture.save()
        # Then
        instances = Picture.objects.all()
        self.assertEqual(1, len(instances))
        self.assertEqual("ExamplePicture.jpg", instances[0].original_name)
        self.assertEqual("unique_identifier-asdf.jpg", instances[0].unique_name)
        self.assertTrue(Path("media/original_pictures/unique_identifier-asdf.jpg").is_file())

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_create_blurred_picture_when_saving_picture_instance(self, _, blurred_image):
        # Given
        with open('tests/helpers/ExamplePicture.jpg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file.read())

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        picture = Picture(picture=uploaded_file)
        # When
        picture.save()
        # Then
        self.assertTrue(Path("media/blurred_pictures/unique_identifier-asdf.jpg").is_file())
        self.assert_images_equal(
            "tests/helpers/loshombresdepacoblurred.png",
            "media/blurred_pictures/unique_identifier-asdf.jpg"
        )

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_delete_images_when_deleting_picture_instance(self, _, blurred_image):
        # Given
        settings.DEBUG = True

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file.read())

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        picture = Picture(picture=uploaded_file)
        picture.save()
        self.assertTrue(Path("media/original_pictures/unique_identifier-asdf.jpg").is_file())
        self.assertTrue(Path("media/blurred_pictures/unique_identifier-asdf.jpg").is_file())
        # When
        picture.delete()
        # Then
        self.assertFalse(Path("media/original_pictures/unique_identifier-asdf.jpg").is_file())
        self.assertFalse(Path("media/blurred_pictures/unique_identifier-asdf.jpg").is_file())

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_delete_picture_instance_does_not_fail_when_images_are_missing(self, _, blurred_image):
        # Given
        settings.DEBUG = True

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file.read())

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        picture = Picture(picture=uploaded_file)
        picture.save()
        os.remove(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg"))
        os.remove(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg"))
        # When
        picture.delete()
        # Then
        self.assertFalse(Path("media/original_pictures/unique_identifier-asdf.jpg").is_file())
        self.assertFalse(Path("media/blurred_pictures/unique_identifier-asdf.jpg").is_file())

    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_delete_picture_instance_does_not_fail_when_images_fields_are_not_set(self, _, blurred_image):
        # Given
        settings.DEBUG = True

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file.read())

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        picture = Picture(picture=uploaded_file)
        picture.save()

        os.remove(os.path.join("media/original_pictures", "unique_identifier-asdf.jpg"))
        os.remove(os.path.join("media/blurred_pictures", "unique_identifier-asdf.jpg"))
        picture.picture = None
        picture.picture_blurred = None
        picture.save()
        # When
        picture.delete()

    @mock.patch("core.models.delete_picture")
    @mock.patch("core.models.blur_faces_of_image")
    @mock.patch("uuid.uuid4", return_value="unique_identifier-asdf")
    def test_delete_images_when_deleting_picture_instance_in_production(self, _, blurred_image, delete_picture):
        # Given
        settings.DEBUG = False

        with open('tests/helpers/ExamplePicture.jpg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file.read())

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        picture = Picture(picture=uploaded_file)
        picture.save()
        # When
        picture.delete()
        # Then
        delete_picture.assert_called_once_with(picture)

    @staticmethod
    def assert_images_equal(expected_file_path, actual_file_path):
        with io.open(actual_file_path, "rb") as actual_image_file:
            actual_image_bytes = actual_image_file.read()
            actual_image = imread(actual_image_bytes, plugin="imageio")

        with io.open(expected_file_path, "rb") as expected_image_file:
            expected_image_bytes = expected_image_file.read()
            expected_image = imread(expected_image_bytes, plugin="imageio")

        np.testing.assert_array_equal(actual_image, expected_image)
