from katadzuke_app_v1.serializers import UserSerializer
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
import numpy as np
from .room_vision import tranlate_rgb_to_csv2
import base64
# Create your views here.

class RoomPhotoUploadAPIView(views.APIView):

    parser_class = [JSONParser, MultiPartParser]

    def post(self, request, *args, **kwargs):

        print(type(request.data["roomPhoto"])) # str
        np_upload_room_photo = np.asarray(bytearray(base64.b64decode( request.data["roomPhoto"].split(',')[1] )), dtype="uint8")
        print(type(np_upload_room_photo))
        print(np_upload_room_photo.shape) # (4274694,)
        print(tranlate_rgb_to_csv2(np_upload_room_photo))

        return Response(status.HTTP_201_CREATED)



class UserCreateAPIView(views.APIView):

    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)