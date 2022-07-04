from django.contrib import admin
from .models import User, RoomPhoto, Reward, FloorHueRange

# Register your models here.

admin.site.register(User)
admin.site.register(RoomPhoto)
admin.site.register(Reward)
admin.site.register(FloorHueRange)
