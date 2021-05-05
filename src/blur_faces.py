from dataclasses import dataclass
import io
from typing import List

import cv2
from google.cloud import vision
import numpy as np


@dataclass
class ImageRectangle:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


def get_face_rectangles(image_bytes: bytes) -> List[ImageRectangle]:

    def bounding_poly_vertices_to_image_rectangle(bounding_poly_vertices):
        top_left_vertex = bounding_poly_vertices[0]
        bottom_right_vertex = bounding_poly_vertices[2]

        return ImageRectangle(
            x_min=top_left_vertex.x,
            x_max=bottom_right_vertex.x,
            y_min=top_left_vertex.y,
            y_max=bottom_right_vertex.y
        )

    response = vision.ImageAnnotatorClient().face_detection(
        image=vision.Image(content=image_bytes)
    )

    return [
        bounding_poly_vertices_to_image_rectangle(face.bounding_poly.vertices)
        for face in response.face_annotations
    ]


def blur_rectangles(image_bytes, rectangles: List[ImageRectangle]):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    for rectangle in rectangles:
        face_region = image[rectangle.y_min:rectangle.y_max, rectangle.x_min:rectangle.x_max]
        blurred_face = cv2.GaussianBlur(face_region, (51, 51), 0)
        image[rectangle.y_min:rectangle.y_max, rectangle.x_min:rectangle.x_max] = blurred_face

    _, im_buf_arr = cv2.imencode(".png", image)

    return im_buf_arr.tobytes()


def read_image(image_file_path: str) -> bytes:
    with io.open(image_file_path, 'rb') as image_file:
        return image_file.read()


def write_image(image_bytes: bytes, image_file_path: str):
    with io.open(image_file_path, "wb") as image_file:
        image_file.write(image_bytes)


def blur_faces(image_file_path, blurred_image_file_path):
    image = read_image(image_file_path)

    face_rectangles = get_face_rectangles(image)

    print(face_rectangles)
    blured_image = blur_rectangles(image, face_rectangles)

    write_image(blured_image, blurred_image_file_path)
