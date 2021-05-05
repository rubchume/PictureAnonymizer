import io

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from core.forms import UploadPictureForm


class UploadPictureView(FormView):
    template_name = "upload_picture.html"
    form_class = UploadPictureForm
    extra_context = {"title": "Upload Picture"}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('upload_picture')}?success=True"
