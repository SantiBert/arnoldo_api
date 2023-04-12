from rest_framework import serializers

from .models import (
    Season, 
    Episodies, 
    EpisodiePicture
    )

class EpisodiePictureSerilizer(serializers.ModelSerializer):
    class Meta:
        model = EpisodiePicture
        fields = ["picture", "is_default"]

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ["id","name","image","banner","description","date","is_active"]
        
class CreateSeasonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    image = serializers.CharField(max_length=600, required=False, allow_null=True)
    banner = serializers.CharField(max_length=600,required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)  

class EditSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = [
            "name",
            "image",
            "banner",
            "description"
            ]

class EpisodiesSerializer(serializers.ModelSerializer):
    season = SeasonSerializer()
    picture = serializers.SerializerMethodField(method_name="get_picture")
    
    def get_picture(self, obj):
        if obj.pictures:
            data = {"picture": obj.pictures, "is_default": True}
            return EpisodiePictureSerilizer(data).data
        else:
            return {}
    
    class Meta:
        model = Episodies
        fields = [
            "id",
            "name",
            "season",
            "description",
            "picture",
            "link1",
            "link2",
            "english",
            "spoty",
            "mediafire"]


class CreateEpisodiesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    season = serializers.IntegerField()
    original_name = serializers.CharField(max_length=150, required=False, allow_null=True)
    original_date = serializers.DateField(required=False, allow_null=True)
    link1 = serializers.URLField(max_length=600, required=False, allow_null=True)
    link2 = serializers.URLField(max_length=600, required=False, allow_null=True)
    english = serializers.URLField(max_length=600, required=False, allow_null=True)
    spoty = serializers.URLField(max_length=600, required=False, allow_null=True)
    mediafire = serializers.URLField(max_length=600, required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)  
    
class EditEpisodiesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150,required=False, allow_null=True)
    season = serializers.IntegerField(required=False, allow_null=True)
    original_name = serializers.CharField(max_length=150, required=False, allow_null=True)
    original_date = serializers.DateField(required=False, allow_null=True)
    link1 = serializers.URLField(max_length=600, required=False, allow_null=True)
    link2 = serializers.URLField(max_length=600, required=False, allow_null=True)
    english = serializers.URLField(max_length=600, required=False, allow_null=True)
    spoty = serializers.URLField(max_length=600, required=False, allow_null=True)
    mediafire = serializers.URLField(max_length=600, required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)  