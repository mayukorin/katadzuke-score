from inspect import CORO_CREATED
from django.core.management.base import BaseCommand
from katadzuke_app_v1.models import User, FloorHueRange


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:

            floor_hue_range = FloorHueRange()
            floor_hue_range.user = user
            floor_hue_range.save()
            
