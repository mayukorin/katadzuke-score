from importlib.util import spec_from_file_location
from logging import raiseExceptions
from .serializers import UserSerializer, RoomPhotoSerializer, RewardSerializer
from .models import RoomPhoto, Reward
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
import numpy as np
from .room_vision import calc_percent_of_floors
import base64, datetime, cloudinary
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
        reward_this_month = Reward.objects.get(recipient=request.user, month=room_photo.filming_date.month)

        if room_photo.photo_public_id is not None:
            cloudinary.uploader.destroy(room_photo.photo_public_id) # cloudinary に id 固定で更新とかない？
            if room_photo.percent_of_floors <= THRESHOULD_FINE_SCORE:
                reward_this_month.amount_of_money += AMOUNT_OF_REWARD
            elif room_photo.percent_of_floors >= THRESHOULD_REWARD_SCORE:
                reward_this_month.amount_of_money -= AMOUNT_OF_FINE

        response = cloudinary.uploader.upload(file=request.data["roomPhotoBase64Content"])
        room_photo.photo_public_id = response["public_id"]
        room_photo.photo_url = response["url"]

        room_photo.percent_of_floors = calc_percent_of_floors(request.data["roomPhotoBase64Content"])

        room_photo.save()

        if room_photo.percent_of_floors <= THRESHOULD_FINE_SCORE:
                reward_this_month.amount_of_money -= AMOUNT_OF_FINE
        elif room_photo.percent_of_floors >= THRESHOULD_REWARD_SCORE:
            reward_this_month.amount_of_money += AMOUNT_OF_REWARD

        reward_this_month.save()

        serializer = RoomPhotoSerializer(instance=room_photo)
       
        '''
        print(type(request.data["roomPhoto"])) # str
        np_upload_room_photo = np.asarray(bytearray(base64.b64decode( request.data["roomPhoto"].split(',')[1] )), dtype="uint8")
        print(type(np_upload_room_photo))
        print(np_upload_room_photo.shape) # (4274694,)
        print(tranlate_rgb_to_csv2(np_upload_room_photo))
        '''

        return Response(serializer.data, status.HTTP_201_CREATED)


class FullScoreRoomPhotoUploadAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        signin_user = request.user
        if signin_user.full_score_photo_public_id is not None:
            cloudinary.uploader.destroy(signin_user.full_score_photo_public_id) # cloudinary に id 固定で更新とかない？

        response = cloudinary.uploader.upload(file=request.data["roomPhotoBase64Content"])
        signin_user.full_score_photo_public_id = response["public_id"]
        signin_user.full_score_photo_url = response["url"]
        signin_user.full_score_room_percent_of_floors = calc_percent_of_floors(request.data["roomPhotoBase64Content"])

        signin_user.save()

        return Response({"full_score_photo_url": signin_user.full_score_photo_url}, status.HTTP_201_CREATED)


class RoomPhotoListAPIView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *arga, **kwargs):

        user_room_photos = RoomPhoto.objects.filter(room_owner=request.user)
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