from importlib.util import spec_from_file_location
from logging import raiseExceptions
from .serializers import UserSerializer, RoomPhotoSerializer, RewardSerializer
from .models import RoomPhoto, Reward
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
import numpy as np
from .room_vision import (
    calc_percent_of_floors,
    upload_room_photo_to_cloudinary,
    destroy_room_photo_from_cloudinary,
    reflect_room_photo_score_to_amount_of_money,
    remove_reflection_of_room_photo_score_from_amount_of_money,
)
import base64, datetime, cloudinary
from django.db.models import Q

# Create your views here.


class RoomPhotoCreateAPIView(views.APIView):

    parser_class = [JSONParser, MultiPartParser]

    def post(self, request, pk, *args, **kwargs):

        # TODO: serializer 使うように変更．serializer.save()のところに入れれば OK
        # 認可を後で追加
        room_photo = RoomPhoto.objects.get(pk=pk)
        serializer = RoomPhotoSerializer(instance=room_photo, data={}, partial=True)
        serializer.is_valid(raise_exception=True)

        if room_photo.photo_public_id is not None:

            destroy_room_photo_from_cloudinary(room_photo.photo_public_id)

        public_id, url = upload_room_photo_to_cloudinary(
            request.data["roomPhotoBase64Content"]
        )
        percent_of_floors = calc_percent_of_floors(
            request.data["roomPhotoBase64Content"]
        )

        serializer.save(
            photo_public_id=public_id,
            percent_of_floors=percent_of_floors,
            photo_url=url,
        )

        return Response(serializer.data, status.HTTP_200_OK)


class RewardThisMonthUpdateAPIView(views.APIView):

    parser_class = [JSONParser, MultiPartParser]

    # TODO: pk で更新できるように変更
    def post(self, request, *args, **kwargs):

        today = datetime.date.today()
        reward_this_month = Reward.objects.get(
            recipient=request.user, month=today.month
        )
        serializer = RewardSerializer(instance=reward_this_month)

        add_amount_this_month = 0

        if request.data["prev_room_photo_score"] is not None:
            add_amount_this_month = reflect_room_photo_score_to_amount_of_money(
                request.user.threshould_fine_score,
                request.user.threshould_reward_score,
                request.user.amount_of_fine,
                request.user.amount_of_reward,
                request.data["new_room_photo_score"],
            ) - remove_reflection_of_room_photo_score_from_amount_of_money(
                request.user.threshould_fine_score,
                request.user.threshould_reward_score,
                request.user.amount_of_fine,
                request.user.amount_of_reward,
                request.data["prev_room_photo_score"],
            )

        serializer.save(
            amount_of_money=reward_this_month.amount_of_money + add_amount_this_month
        )

        return Response(serializer.data, status.HTTP_200_OK)


class RoomPhotoListAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *arga, **kwargs):

        user_room_photos = RoomPhoto.objects.filter(room_owner=request.user).filter(
            ~Q(pk=request.user.full_score_photo.pk)
        )
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

        serializer = UserSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)
