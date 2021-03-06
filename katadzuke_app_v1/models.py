from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime, cloudinary


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

            if date.weekday() >= 6:
                # 日曜日まで作ったら終わり
                break

        full_score_room_photo = RoomPhoto()
        full_score_room_photo.filming_date = today
        full_score_room_photo.room_owner = user
        full_score_room_photo.save()
        user.full_score_photo = full_score_room_photo
        user.save()

        floor_hue_range = FloorHueRange()
        floor_hue_range.user = user
        floor_hue_range.save()

        floor_photo = FloorPhoto()
        floor_photo.photo_owner = user
        floor_photo.save()

        reward, created = Reward.objects.get_or_create(
            month=today.month, recipient=user
        )
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
    threshould_reward_score = models.IntegerField(
        default=70, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    threshould_fine_score = models.IntegerField(
        default=30, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    amount_of_reward = models.IntegerField(default=500)
    amount_of_fine = models.IntegerField(default=500)
    full_score_photo = models.OneToOneField(
        "RoomPhoto", on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def get_amount_of_reward_this_month(self):
        today = datetime.date.today()
        reward_this_month = Reward.objects.get(recipient=self, month=today.month)
        return reward_this_month.amount_of_money

    def calc_reward_of_room_photo_score(self, room_photo_score):

        reward = 0

        if room_photo_score <= self.threshould_fine_score:
            reward -= self.amount_of_fine
        elif room_photo_score >= self.threshould_reward_score:
            reward += self.amount_of_reward

        return reward

    def update_reward_of_today_of_week_room_photo_score(self, new_room_photo_score, prev_room_photo_score):

        reward = self.calc_reward_of_room_photo_score(
            room_photo_score=new_room_photo_score
        )

        if prev_room_photo_score is not None:
            reward -= self.calc_reward_of_room_photo_score(
                room_photo_score=prev_room_photo_score
            )

        return reward



class RoomPhoto(models.Model):

    filming_date = models.DateField()
    photo_url = models.CharField(null=True, blank=True, max_length=255)
    photo_public_id = models.CharField(null=True, blank=True, max_length=255)
    room_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    percent_of_floors = models.IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def get_katadzuke_score(self):
        print(self.room_owner.full_score_photo.percent_of_floors)
        if self.percent_of_floors is not None:
            if self.room_owner.full_score_photo.percent_of_floors is None:
                return self.percent_of_floors
            elif self.room_owner.full_score_photo.percent_of_floors == 0:
                return 100
            else:
                return int(
                    100
                    * (
                        min(
                            self.percent_of_floors
                            / self.room_owner.full_score_photo.percent_of_floors,
                            1,
                        )
                    )
                )
        else:
            return None

    def set_percent_of_floors_and_photo_public_id_and_photo_url(
        self, percent_of_floors, public_id, url
    ):

        self.percent_of_floors = percent_of_floors
        self.photo_public_id = public_id
        self.photo_url = url
        self.save()

        return self

    def reset_percent_of_floors_and_photo_public_id_and_photo_url(self):

        self.photo_public_id = ""
        self.photo_url = ""  # TODO :null条件にひっかからないかも
        self.percent_of_floors = 0

        self.save()

        return self

    def destroy_room_photo_from_cloudinary(self):

        cloudinary.uploader.destroy(self.photo_public_id)

class FloorPhoto(models.Model):

    photo_url = models.CharField(null=True, blank=True, max_length=255)
    photo_public_id = models.CharField(null=True, blank=True, max_length=255)
    photo_owner = models.ForeignKey(User, on_delete=models.CASCADE)


class FloorHueRange(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_hue = models.IntegerField(default=14, validators=[MinValueValidator(0), MaxValueValidator(720)])
    max_hue = models.IntegerField(default=17, validators=[MinValueValidator(0), MaxValueValidator(720)])



class Reward(models.Model):

    month = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)]
    )
    amount_of_money = models.IntegerField(default=0)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    def reflect_room_photo_score_to_amount_of_money(self, new_room_photo_score):

        if new_room_photo_score <= self.recipient.threshould_fine_score:
            self.amount_of_money -= self.recipient.amount_of_fine
        elif new_room_photo_score >= self.recipient.threshould_reward_score:
            self.amount_of_money += self.recipient.amount_of_reward

        self.save()

        return self

    def remove_reflection_of_room_photo_score_from_amount_of_money(
        self, prev_room_photo_score
    ):

        if prev_room_photo_score <= self.recipient.threshould_fine_score:
            self.amount_of_money += self.recipient.amount_of_fine
        elif prev_room_photo_score >= self.recipient.threshould_reward_score:
            self.amount_of_money -= self.recipient.amount_of_reward

        self.save()

        return self
