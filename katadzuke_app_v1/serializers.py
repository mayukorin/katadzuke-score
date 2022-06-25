import katadzuke_app_v1
from rest_framework import serializers
from .models import RoomPhoto, User, Reward
import re
from django.core.exceptions import ObjectDoesNotExist

class RoomPhotoSerializer(serializers.ModelSerializer):

    katadzuke_score = serializers.SerializerMethodField()

    class Meta:
        model = RoomPhoto
        fields = ['filming_date', 'photo_url', 'percent_of_floors', 'pk', 'katadzuke_score', 'photo_public_id']

        extra_kwargs = {
            'filming_date': {
                'read_only': True
            },
            'photo_url': {
                'read_only': True
            },
            'percent_of_floors': {
                'read_only': True
            },
            'pk': {
                'read_only': True
            },
            'katadzuke_score': {
                'read_only': True
            },
        }

    def get_katadzuke_score(self, instance):
        return instance.get_katadzuke_score()

class UserSerializer(serializers.ModelSerializer):

    full_score_photo = RoomPhotoSerializer(read_only=True)
    amount_of_reward_this_month = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'threshould_reward_score', 'threshould_fine_score', 'amount_of_reward', 'amount_of_fine', 'full_score_photo', 'amount_of_reward_this_month']

        extra_kwargs = {
            'email': {
                'error_messages': {
                    'blank': 'メールアドレスを入力してください',
                }
            },
            'username': {
                'write_only': True,
                'error_messages': {
                    'blank': 'ユーザー名を入力してください',
                }
            },
            'password': {
                'write_only': True,
                'error_messages': {
                    'blank': 'パスワードを入力してください',
                }
            },
        }

    def validate_email(self, value):
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise serializers.ValidationError('メールアドレスの書式が正しくありません。')
        try:
            user = User.objects.get(email=value)
        except ObjectDoesNotExist:
            return value
        else:
            raise serializers.ValidationError('入力されたメールアドレスはすでに使用されています。')


    def create(self, validated_data):
        return User.objects.create_user(email=validated_data["email"], password=validated_data["password"], username=validated_data["username"])

    def get_amount_of_reward_this_month(self, instance):
        return instance.get_amount_of_reward_this_month()



class RewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = ['month', 'amount_of_money', 'pk']

        extra_kwargs = {
            'month': {
                'read_only': True
            },
            'amount_of_money': {
                'read_only': True
            },
            'pk': {
                'read_only': True
            }
        }