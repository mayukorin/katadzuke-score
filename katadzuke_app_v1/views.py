from importlib.util import spec_from_file_location
from logging import raiseExceptions
from .serializers import (
    UserSerializer,
    RoomPhotoSerializer,
    RewardSerializer,
    FloorPhotoSerializer,
)
from .models import RoomPhoto, Reward, FloorPhoto, FloorHueRange
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
import numpy as np
from .room_vision import (
    reflect_room_photo_score_to_amount_of_money,
    remove_reflection_of_room_photo_score_from_amount_of_money,
    calc_upload_floor_photo_hue_cnt_list,
    merge_floor_hue_ranges_into_upload_floor_photo_hue_cnt_list,
    create_new_hue_ranges_model,
)
from .utils import (
    calc_percent_of_floors_of_photo,
    replace_current_cloudinary_photo_with_posted_photo,
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

        (
            public_id_of_photo_uploaded_to_cloudinary,
            url_of_photo_uploaded_to_cloudinary,
        ) = replace_current_cloudinary_photo_with_posted_photo(
            public_id_of_current_cloudinary_photo=room_photo.photo_public_id,
            base64_content_of_posted_photo=request.data["roomPhotoBase64Content"],
        )

        floor_hue_ranges=FloorHueRange.objects.filter(user=request.user)
        floor_hue_ranges_list = []
        for floor_hue_range in floor_hue_ranges:
            floor_hue_ranges_list.append(floor_hue_range.min_hue)
            floor_hue_ranges_list.append(floor_hue_range.max_hue)


        percent_of_floors = calc_percent_of_floors_of_photo(
            base64_content=request.data["roomPhotoBase64Content"],
            floor_hue_ranges_list=floor_hue_ranges_list,
        )

        serializer.save(
            photo_public_id=public_id_of_photo_uploaded_to_cloudinary,
            percent_of_floors=percent_of_floors,
            photo_url=url_of_photo_uploaded_to_cloudinary,
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

        add_reward_this_month = request.user.update_reward_of_today_of_week_room_photo_score(new_room_photo_score=request.data["new_room_photo_score"], prev_room_photo_score=request.data["prev_room_photo_score"])

        serializer.is_valid(raise_exception=True)

        serializer.save(
            amount_of_money=reward_this_month.amount_of_money + add_reward_this_month
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

        (
            public_id_of_photo_uploaded_to_cloudinary,
            url_of_photo_uploaded_to_cloudinary,
        ) = replace_current_cloudinary_photo_with_posted_photo(
            public_id_of_current_cloudinary_photo=floor_photo.photo_public_id,
            base64_content_of_posted_photo=request.data["floorPhotoBase64Content"],
        )

        serializer.save(
            photo_public_id=public_id_of_photo_uploaded_to_cloudinary,
            photo_url=url_of_photo_uploaded_to_cloudinary,
        )

        floor_hue_ranges = FloorHueRange.objects.filter(user=request.user)
        hue_floor_pixel_cnt_list = (
            merge_floor_hue_ranges_into_upload_floor_photo_hue_cnt_list(
                floor_hue_ranges,
                calc_upload_floor_photo_hue_cnt_list(
                    request.data["floorPhotoBase64Content"]
                ),
            )
        )

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
