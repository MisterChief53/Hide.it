from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload-video/", views.upload_video, name="upload_video"),
    path("video/", views.lookForVideo, name="lookForVideo"),
]