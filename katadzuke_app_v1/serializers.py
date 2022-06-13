import katadzuke_app_v1
from rest_framework import serializers
from .models import RoomPhoto, User, Reward
import re
from django.core.exceptions import ObjectDoesNotExist

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'full_score_photo_url', 'threshould_reward_score', 'threshould_fine_score', 'amount_of_reward', 'amount_of_fine']

        extra_kwargs = {
            'full_score_photo_url': {
                'read_only': True
            },
            'email': {
                'write_only': True
            },
            'username': {
                'write_only': True
            },
            'password': {
                'write_only': True
            }
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

    def validate_password(self, value):
        if value == '':
            raise serializers.ValidationError('パスワードを入力してください')
        return value

    def validate_username(self, value):
        if value == '':
            raise serializers.ValidationError('ユーザー名を入力してください')

        return value

    def create(self, validated_data):
        # serializer.save() で呼ばれる
        return User.objects.create_user(email=validated_data["email"], password=validated_data["password"], username=validated_data["username"])



class RoomPhotoSerializer(serializers.ModelSerializer):

    katadzuke_score = serializers.SerializerMethodField()

    class Meta:
        model = RoomPhoto
        fields = ['filming_date', 'photo_url', 'percent_of_floors', 'pk', 'katadzuke_score']

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