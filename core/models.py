import io
import os
import uuid

from core.google_cloud_picture_storage import delete_picture
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import models
from django.dispatch import receiver

from src.blur_faces import blur_faces_of_image


def generate_unique_name(filename):
    ext = filename.split('.')[-1]
    return f"{str(uuid.uuid4())}.{ext}"


class Picture(models.Model):
    picture = models.ImageField(upload_to="original_pictures")
    unique_name = models.CharField(max_length=255, null=False, blank=False)
    original_name = models.CharField(max_length=255, null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    picture_blurred = models.ImageField(upload_to="blurred_pictures", null=True, blank=True)

    def blur_faces_in_picture(self):
        original_picture_image = self.picture.file.read()
        blurred_picture_image = blur_faces_of_image(original_picture_image)

        blurred_picture_file = ImageFile(io.BytesIO(blurred_picture_image), name=self.unique_name)

        self.picture_blurred = blurred_picture_file

    def save(self, *args, **kwargs):
        if not self.pk:
            original_name = self.picture.name
            unique_name = generate_unique_name(original_name)

            self.picture.name = unique_name
            self.unique_name = unique_name
            self.original_name = original_name

            self.blur_faces_in_picture()

        return super(Picture, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Picture)
def auto_delete_picture_file_on_delete(sender, instance, **kwargs):
    if not settings.DEBUG:
        delete_picture(instance)
    else:
        if instance.picture:
            if os.path.isfile(instance.picture.path):
                os.remove(instance.picture.path)

        if instance.picture_blurred:
            if os.path.isfile(instance.picture_blurred.path):
                os.remove(instance.picture_blurred.path)
