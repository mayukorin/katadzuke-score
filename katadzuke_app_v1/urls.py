from django.contrib import admin
from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('signup/', views.UserCreateAPIView.as_view()),
    path('room-photos/<str:pk>/room-photo-upload/', views.RoomPhotoCreateAPIView.as_view()),
    path('room-photos/', views.RoomPhotoListAPIView.as_view()),
    path('room-photos/full-score/', views.FullScoreRoomPhotoUploadAPIView.as_view()),
    path('reward-this-month-update/', views.RewardThisMonthUpdateAPIView.as_view()),
    path('reward-this-month/', views.RewardThisMonthGetAPIView.as_view()),
    path('user-info/', views.UserInfoGetAPIView.as_view()), # TODO: 名前イマイチ?
    path('user-info-update/', views.UserInfoUpdateAPIView.as_view())
]
