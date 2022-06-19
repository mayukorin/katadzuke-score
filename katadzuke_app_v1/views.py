from importlib.util import spec_from_file_location
from logging import raiseExceptions
from .serializers import UserSerializer, RoomPhotoSerializer, RewardSerializer
from .models import RoomPhoto, Reward
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
import numpy as np
from .room_vision import calc_percent_of_floors, upload_room_photo_to_cloudinary
import base64, datetime, cloudinary
from django.db.models import Q
# Create your views here.

THRESHOULD_REWARD_SCORE = 60
THRESHOULD_FINE_SCORE = 20

AMOUNT_OF_REWARD = 100
AMOUNT_OF_FINE = 200

class RoomPhotoCreateAPIView(views.APIView):

    parser_class = [JSONParser, MultiPartParser]

    def post(self, request, pk, *args, **kwargs):
        
        # serializer 使うように後で変更
        # 認可を後で追加
        # room_photo の update と，reward の update は別にした方が良い？
        room_photo = RoomPhoto.objects.get(pk=pk) 
        # reward_this_month = Reward.objects.get(recipient=request.user, month=room_photo.filming_date.month)

        if room_photo.photo_public_id is not None:

            room_photo.destroy_room_photo_from_cloudinary()
            room_photo.reset_percent_of_floors_and_photo_public_id_and_photo_url()
            # reward_this_month.remove_reflection_of_room_photo_score_from_amount_of_money(room_photo)

        public_id, url = upload_room_photo_to_cloudinary(request.data["roomPhotoBase64Content"])
        percent_of_floors = calc_percent_of_floors(request.data["roomPhotoBase64Content"])
        room_photo = room_photo.set_percent_of_floors_and_photo_public_id_and_photo_url(percent_of_floors, public_id, url)
        
        # reward_this_month.reflect_room_photo_score_to_amount_of_money(room_photo)

        serializer = RoomPhotoSerializer(instance=room_photo)
       

        return Response(serializer.data, status.HTTP_201_CREATED)

class RewardThisMonthUpdateAPIView(views.APIView):

    parser_class = [JSONParser, MultiPartParser]

    #TODO: pk で更新できるように変更
    def post(self, request, *args, **kwargs):

        today = datetime.date.today()
        reward_this_month = Reward.objects.get(recipient=request.user, month=today.month)
        print(request.data["prev_room_photo_score"])
        print(request.data["new_room_photo_score"])
        reward_this_month = reward_this_month.remove_reflection_of_room_photo_score_from_amount_of_money(request.data["prev_room_photo_score"])
        reward_this_month.reflect_room_photo_score_to_amount_of_money(request.data["new_room_photo_score"])

        serializer = RewardSerializer(instance=reward_this_month)
        return Response(serializer.data, status.HTTP_201_CREATED)




class FullScoreRoomPhotoUploadAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        signin_user = request.user
        if signin_user.full_score_photo.photo_public_id is not None:
            signin_user.full_score_photo.destroy_room_photo_from_cloudinary()


        public_id, url = upload_room_photo_to_cloudinary(request.data["roomPhotoBase64Content"])
        percent_of_floors = calc_percent_of_floors(request.data["roomPhotoBase64Content"])
        signin_user.full_score_photo.set_percent_of_floors_and_photo_public_id_and_photo_url(percent_of_floors, public_id, url)

        serializer = RoomPhotoSerializer(instance=signin_user.full_score_photo)

        return Response(serializer.data, status.HTTP_201_CREATED) # TODO: CREATED?


class RoomPhotoListAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *arga, **kwargs):

        user_room_photos = RoomPhoto.objects.filter(room_owner=request.user).filter(~Q(pk=request.user.full_score_photo.pk))
        serializer = RoomPhotoSerializer(instance=user_room_photos, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class UserCreateAPIView(views.APIView):


    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class UserInfoGetAPIView(views.APIView):

    # TODO: jwt のやつに組み込めないのか

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        serializer = UserSerializer(instance=request.user)

        return Response(serializer.data, status.HTTP_200_OK)

class UserInfoUpdateAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):

        print(request.data)
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class RewardThisMonthGetAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        today = datetime.date.today()
        reward_this_month = Reward.objects.get(recipient=request.user, month=today.month)
        serializer = RewardSerializer(instance=reward_this_month)
        return Response(serializer.data, status.HTTP_200_OK)