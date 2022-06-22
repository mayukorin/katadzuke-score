from inspect import CORO_CREATED
from django.core.management.base import BaseCommand
import datetime, cloudinary
from katadzuke_app_v1.models import User, RoomPhoto, Reward


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.date.today()
        users = User.objects.all()

        for user in users:
            
            room_photo = RoomPhoto()
            room_photo.filming_date = today 
            room_photo.room_owner = user 
            room_photo.save()
            print(room_photo)
            user.full_score_photo = room_photo
            print(user.full_score_photo)
            user.save()
            print(user.full_score_photo)
                   