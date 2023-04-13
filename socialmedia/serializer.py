from rest_framework import serializers

from .models import (
    SocialMedia, 
    EnlaceSocial,
    )

from django.core.exceptions import PermissionDenied

from rest_framework import permissions
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response


class SocialMediaSerilizer(serializers.ModelSerializer):
    
    link = serializers.SerializerMethodField(method_name="get_link")
    
    def get_link(self, obj):
        data = EnlaceSocial.objects.get(social_media=obj)
        return data.link
    
    class Meta:
        model = SocialMedia
        fields = ["name", "icon", "link"]


class SocialMediaCreateSerilizer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    icon = serializers.CharField(max_length=150, required=False, allow_null=True)
    link = serializers.URLField(max_length=150)

class SocialMediaEditSerilizer(serializers.Serializer):
    name = serializers.CharField(max_length=150,required=False, allow_null=True)
    icon = serializers.CharField(max_length=150, required=False, allow_null=True)
    link = serializers.URLField(max_length=150, required=False, allow_null=True)