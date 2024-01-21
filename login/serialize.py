from rest_framework import serializers
from .models import LoginUser
from django.contrib.auth.hashers import make_password

class LoginUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data): # validated_data = 입력 받은 데이터를 직렬화시킨 데이터
        validated_data['user_pw'] = make_password(validated_data['user_pw'])
        user = LoginUser.objects.create(**validated_data) # 직렬화된 데이터를 통해 Django 모델 생성
        return user # Django 모델 반환
    
    def validate(self, attrs):
        return attrs
    
    class Meta:
        model = LoginUser
        fields = ('user_id', 'user_pw', 'birth_day', 'gender', 'email', 'name', 'age')
    