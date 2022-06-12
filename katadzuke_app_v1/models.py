from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        today = datetime.date.today()

        # RoomPhotoとの結合度が高くなってしまい，良くない？
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

        reward, created = Reward.objects.get_or_create(month=today.month, recipient=user)
        reward.amount_of_money = 0
        reward.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    email = models.EmailField(
        verbose_name="メールアドレス",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(verbose_name="ユーザ名", max_length=150)
    full_score_photo_public_id = models.CharField(null=True, blank=True, max_length=255)
    full_score_photo_url = models.CharField(null=True, blank=True, max_length=255)
    full_score_room_percent_of_floors = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    threshould_reward_score = models.IntegerField(default=70, validators=[MinValueValidator(0), MaxValueValidator(100)])
    threshould_fine_score = models.IntegerField(default=30, validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount_of_reward = models.IntegerField(default=500)
    amount_of_fine = models.IntegerField(default=500)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

class RoomPhoto(models.Model):

    filming_date = models.DateField()
    photo_url = models.CharField(null=True, blank=True, max_length=255)
    photo_public_id = models.CharField(null=True, blank=True, max_length=255)
    room_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    percent_of_floors = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def get_katadzuke_score(self):
        print(self.room_owner.full_score_room_percent_of_floors)
        if self.percent_of_floors is not None:
            if self.room_owner.full_score_room_percent_of_floors is None:
                return self.percent_of_floors
            elif self.room_owner.full_score_room_percent_of_floors == 0:
                return 100
            else:
                return int(100*(min(self.percent_of_floors/self.room_owner.full_score_room_percent_of_floors, 1)))
        else:
            return None


class Reward(models.Model):

    month = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    amount_of_money = models.IntegerField(default=0)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
