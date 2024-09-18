from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_video, name='upload_video'),
    path("fetch/<int:video_id>", views.fetch_video, name='fetch_video'),
    path("delete/<int:video_id>", views.delete_video, name='delete_video'),
    path('search/', views.search_subtitles, name='search_subtitles'),
]