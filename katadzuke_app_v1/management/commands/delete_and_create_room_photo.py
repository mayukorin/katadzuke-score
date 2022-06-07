from inspect import CORO_CREATED
from django.core.management.base import BaseCommand
import datetime, cloudinary
from katadzuke_app_v1.models import User, RoomPhoto, Reward


class Command(BaseCommand):
    def handle(self, *args, **options):
        # today = datetime.date.today()
        today = datetime.date(2022, 6, 1)
        if today.day == 1 or today.weekday() == 0:
            
            users = User.objects.all()

            for user in users:
                
                for add_day in range(7):
                    date = today + datetime.timedelta(days=add_day)
                    room_photo = RoomPhoto()
                    room_photo.filming_date = date 
                    room_photo.room_owner = user 
                    room_photo.save()
                    print(date)
                    print(date.weekday())

                    if date.weekday() >= 6:
                        # 日曜日まで作ったら終わり
                        break

            
                room_photos = RoomPhoto.objects.filter(room_owner=user, filming_date__lt=today)
                for room_photo in room_photos:
                    print(room_photo.filming_date)
                    # cloudinary.uploader.destroy(room_photo.photo_public_id)
                    room_photo.delete()


                if today.day == 1:
                    reward, created = Reward.objects.get_or_create(month=today.month, recipient=user)
                    reward.amount_of_money = 0
                    reward.save()
