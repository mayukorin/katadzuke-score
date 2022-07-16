from importlib.util import spec_from_file_location
from logging import raiseExceptions
from .serializers import UserSerializer, RoomPhotoSerializer, RewardSerializer, FloorPhotoSerializer
from .models import RoomPhoto, Reward, FloorPhoto, FloorHueRange
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
import numpy as np
from .room_vision import (
    calc_percent_of_floors,
    upload_photo_to_cloudinary,
    destroy_photo_from_cloudinary,
    reflect_room_photo_score_to_amount_of_money,
    remove_reflection_of_room_photo_score_from_amount_of_money,
    calc_upload_floor_photo_hue_cnt_list,
    merge_floor_hue_ranges_into_upload_floor_photo_hue_cnt_list,
    create_new_hue_ranges_model
)
import datetime
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

            destroy_photo_from_cloudinary(room_photo.photo_public_id)

        public_id, url = upload_photo_to_cloudinary(
            request.data["roomPhotoBase64Content"]
        )

        floor_hue_ranges = FloorHueRange.objects.filter(user=request.user)

        floor_hue_ranges_list = []

        for floor_hue_range in floor_hue_ranges:
            floor_hue_ranges_list.append(floor_hue_range.min_hue)
            floor_hue_ranges_list.append(floor_hue_range.max_hue)

        percent_of_floors = calc_percent_of_floors(
            request.data["roomPhotoBase64Content"],
            floor_hue_ranges_list
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
        serializer = RewardSerializer(instance=reward_this_month, data={}, partial=True)

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

        serializer.is_valid(raise_exception=True)

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

class FloorPhotoGetAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *arga, **kwargs):

        floor_photo = FloorPhoto.objects.get(photo_owner=request.user)
        print(floor_photo)
        serializer = FloorPhotoSerializer(instance=floor_photo)

        return Response(serializer.data, status.HTTP_200_OK)

class FloorPhotoUploadAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        
        # TODO: 認可追加
        floor_photo = FloorPhoto.objects.get(pk=pk)
        serializer = FloorPhotoSerializer(instance=floor_photo, data={}, partial=True)
        serializer.is_valid(raise_exception=True)

        if floor_photo.photo_public_id is not None:

            destroy_photo_from_cloudinary(floor_photo.photo_public_id)

        public_id, url = upload_photo_to_cloudinary(
            request.data["floorPhotoBase64Content"]
        )

        serializer.save(
            photo_public_id=public_id,
            photo_url=url,
        )




        floor_hue_ranges = FloorHueRange.objects.filter(user=request.user)
        hue_floor_pixel_cnt_list = merge_floor_hue_ranges_into_upload_floor_photo_hue_cnt_list(floor_hue_ranges, calc_upload_floor_photo_hue_cnt_list(request.data["floorPhotoBase64Content"]))

        floor_hue_ranges.delete()

        create_new_hue_ranges_model(hue_floor_pixel_cnt_list, request.user)


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
