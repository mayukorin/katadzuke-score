from django.contrib import admin
from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('signup/', views.UserCreateAPIView.as_view()),
    path('room-photos/<str:pk>/room-photo-upload/', views.RoomPhotoCreateAPIView.as_view()),
    path('room-photos/', views.RoomPhotoListAPIView.as_view()),
    path('reward-this-month/', views.RewardThisMonthGetAPIView.as_view()),
]
