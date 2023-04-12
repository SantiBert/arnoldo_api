# serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('nickname', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomLoginSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        nickname = data.get('nickname', None)
        password = data.get('password', None)

        if nickname is None or password is None:
            raise serializers.ValidationError(
                'Debe proporcionar un correo electrónico y una contraseña.'
            )

        user = authenticate(username=nickname, password=password)

        if user is None:
            raise serializers.ValidationError(
                'No se encontró un usuario con estas credenciales.'
            )

        token, created = Token.objects.get_or_create(user=user)

        return {
            'user': CustomUserSerializer(user).data,
            'token': token.key
        }
