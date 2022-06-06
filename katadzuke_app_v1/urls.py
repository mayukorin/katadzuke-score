from django.contrib import admin
from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('signup/', views.UserCreateAPIView.as_view()),
    path('room-photo-upload/', views.RoomPhotoUploadAPIView.as_view()),
]
