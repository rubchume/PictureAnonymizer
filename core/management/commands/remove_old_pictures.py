from datetime import timedelta

from core.models import Picture
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Removes old pictures"

    def add_arguments(self, parser):
        parser.add_argument('max_picture_storage_minutes', nargs='?', type=int)

    def handle(self, *args, **options):
        max_picture_storage_minutes = options.get("max_picture_storage_minutes", settings.MAX_PICTURE_STORAGE_MINUTES)
        if not max_picture_storage_minutes:
            max_picture_storage_minutes = settings.MAX_PICTURE_STORAGE_MINUTES

        old_pictures = Picture.objects.filter(uploaded_at__lte=timezone.now() - timedelta(minutes=max_picture_storage_minutes))
        for picture in old_pictures:
            picture.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted old pictures'))
