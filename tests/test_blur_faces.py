import io
import os
import unittest
from unittest import mock

import google
import numpy as np
from skimage.io import imread

from src.blur_faces import blur_faces


class BlurFacesTests(unittest.TestCase):

    @mock.patch("google.cloud.vision.ImageAnnotatorClient")
    def test_blur_face_calls_google_cloud_platform_vision_api_and_applies_gaussian_blur(self, google_client):
        # Given
        face_detection_response = mock.MagicMock()
        face1 = mock.MagicMock()
        face2 = mock.MagicMock()
        face3 = mock.MagicMock()
        face4 = mock.MagicMock()
        face_detection_response.face_annotations = [
            face1, face2, face3, face4
        ]
        face1.bounding_poly = google.cloud.vision_v1.types.geometry.BoundingPoly(
            dict(vertices=[
                dict(x=337, y=159),
                dict(x=466, y=159),
                dict(x=466, y=309),
                dict(x=337, y=309),
            ])
        )
        face2.bounding_poly = google.cloud.vision_v1.types.geometry.BoundingPoly(
            dict(vertices=[
                dict(x=480, y=144),
                dict(x=615, y=144),
                dict(x=615, y=301),
                dict(x=480, y=301),
            ])
        )
        face3.bounding_poly = google.cloud.vision_v1.types.geometry.BoundingPoly(
            dict(vertices=[
                dict(x=676, y=48),
                dict(x=833, y=48),
                dict(x=833, y=231),
                dict(x=676, y=231),
            ])
        )
        face4.bounding_poly = google.cloud.vision_v1.types.geometry.BoundingPoly(
            dict(vertices=[
                dict(x=113, y=81),
                dict(x=303, y=81),
                dict(x=303, y=302),
                dict(x=113, y=302),
            ])
        )
        face_detection = mock.MagicMock()
        face_detection.return_value = face_detection_response
        google_client_instance = mock.MagicMock()
        google_client.return_value = google_client_instance
        google_client_instance.face_detection = face_detection
        # When
        blur_faces("tests/helpers/loshombresdepaco.jpeg", "tests/helpers/blurred.png")
        # Then
        with io.open("tests/helpers/blurred.png", "rb") as blurred_image_file:
            blurred_image_bytes = blurred_image_file.read()
            blurred_image = imread(blurred_image_bytes, plugin="imageio")

        with io.open("tests/helpers/loshombresdepacoblurred.png", "rb") as expected_image_file:
            expected_image_bytes = expected_image_file.read()
            expected_image = imread(expected_image_bytes, plugin="imageio")

        np.testing.assert_array_almost_equal(blurred_image / 255, expected_image / 255, decimal=2)

        # Finally
        if os.path.exists("tests/helpers/blurred.png"):
            os.remove("tests/helpers/blurred.png")
