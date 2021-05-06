from django.contrib import admin

from .models import Picture


class PictureAdmin(admin.ModelAdmin):
    list_display = ['picture', "original_name", "unique_name", "uploaded_at"]


admin.site.register(Picture, PictureAdmin)
