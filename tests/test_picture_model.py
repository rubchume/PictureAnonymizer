import io
import os
from pathlib import Path
import time
import unittest
from unittest import mock

from core.models import Picture
import cv2
from django.core.files.uploadedfile import SimpleUploadedFile
import numpy as np
import pytest


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
    def test_create_blur_picture_faces_in_background(self, _, blurred_image):
        # Given
        with open('tests/helpers/ExamplePicture.jpg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('ExamplePicture.jpg', file.read())

        with open("tests/helpers/loshombresdepacoblurred.png", "rb") as file:
            blurred_image.return_value = file.read()

        picture = Picture(picture=uploaded_file)
        # When
        picture.save()
        # Then
        time.sleep(1)
        self.assertTrue(Path("media/blurred_pictures/unique_identifier-asdf.jpg").is_file())
        self.assert_images_equal(
            "tests/helpers/loshombresdepacoblurred.png",
            "media/blurred_pictures/unique_identifier-asdf.jpg"
        )

    @staticmethod
    def assert_images_equal(expected_file_path, actual_file_path):
        with io.open(actual_file_path, "rb") as actual_image_file:
            actual_image_bytes = actual_image_file.read()
            nparr = np.frombuffer(actual_image_bytes, np.uint8)
            actual_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        with io.open(expected_file_path, "rb") as expected_image_file:
            expected_image_bytes = expected_image_file.read()
            nparr = np.frombuffer(expected_image_bytes, np.uint8)
            expected_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        np.testing.assert_array_equal(actual_image, expected_image)
