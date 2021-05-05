import uuid

from django.db import models


def generate_unique_name(instance, filename):
    ext = filename.split('.')[-1]
    return f"original_pictures/{str(uuid.uuid4())}.{ext}"


class Picture(models.Model):
    picture = models.ImageField(upload_to=generate_unique_name)
    uploaded_at = models.DateTimeField(auto_now_add=True)
