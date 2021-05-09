from google.cloud import storage
from django.conf import settings


def delete_picture(instance):
    client = storage.Client()
    bucket = client.get_bucket(settings.GS_BUCKET_NAME)

    if instance.picture:
        blob = bucket.blob(instance.picture.name)
        if blob.exists(client):
            blob.delete()

    if instance.picture_blurred:
        blob = bucket.blob(instance.picture_blurred.name)
        if blob.exists(client):
            blob.delete()
