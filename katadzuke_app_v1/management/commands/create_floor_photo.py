from inspect import CORO_CREATED
from django.core.management.base import BaseCommand
from katadzuke_app_v1.models import User, FloorPhoto


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:

            floor_photo = FloorPhoto()
            floor_photo.photo_owner = user
            floor_photo.save()
            
