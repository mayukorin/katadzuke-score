from rest_framework import serializers
from .models import User
import re
from django.core.exceptions import ObjectDoesNotExist

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

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