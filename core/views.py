from core.forms import UploadPictureForm
from core.models import Picture
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, RedirectView


class HomeView(RedirectView):
    url = reverse_lazy("upload_picture")


class UploadPictureView(FormView):
    template_name = "upload_picture.html"
    form_class = UploadPictureForm
    extra_context = {"title": "Upload Picture"}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('upload_picture')}?success=True"


class DashboardView(ListView):
    template_name = "dashboard.html"
    model = Picture
    extra_context = {"title": "Dashboard"}
    context_object_name = "pictures"
