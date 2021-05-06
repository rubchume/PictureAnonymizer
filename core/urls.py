from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload_picture/', views.UploadPictureView.as_view(), name='upload_picture'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
