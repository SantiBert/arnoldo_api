from django.core.exceptions import PermissionDenied

from rest_framework import permissions
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import (
    Season, 
    Episodies, 
    EpisodiePicture
    )

from .serializer import (
    EpisodiePictureSerilizer,
    SeasonSerializer,
    EpisodiesSerializer,
    CreateSeasonSerializer,
    CreateEpisodiesSerializer,
    EditSeasonSerializer,
    EditEpisodiesSerializer,
)

from .filters import EpisodiesFilter

class GetSeasonsDataView(GenericAPIView):
    
    serializer_class = SeasonSerializer

    def get(self, request):
        try:
            seasons = Season.objects.filter(is_active=True)
            serializer = SeasonSerializer(seasons,many=True)
            return Response({"seasons": serializer.data}, status=200)
        except Season.DoesNotExist:
            return Response({"error": "Seasons does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class GetSeasonDataView(GenericAPIView):
    
    serializer_class = SeasonSerializer

    def get(self, request, season_id):
        try:
            season = Season.objects.get(id=season_id,is_active=True)
            serializer = SeasonSerializer(season)
            return Response({"data": serializer.data}, status=200)
        except Season.DoesNotExist:
            return Response({"error": "Seasons does not exist"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CreateSeasonView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateSeasonSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        try:
            name = serializer.validated_data["name"]
            image = serializer.validated_data["image"]
            banner = serializer.validated_data["banner"]
            description = serializer.validated_data["description"]
            
            season = Season.objects.create(
                name=name,
                image=image,
                banner=banner,
                description=description
            )
            
            result_serializer = SeasonSerializer(season)
            
            return Response({"data": result_serializer.data}, status=200)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class EditSeasonView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditSeasonSerializer

    def post(self, request, season_id):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        try:
            name = serializer.validated_data["name"]
            image = serializer.validated_data["image"]
            banner = serializer.validated_data["banner"]
            description = serializer.validated_data["description"]
            
            season = Season.objects.get(
                id=season_id,
                is_active=True
            )
            if name:
                season.name = name
            if image:
                season.image = image
            if banner:
                season.banner = banner
            if description:
                season.description = description
            
            season.save()
            result_serializer = SeasonSerializer(season)
            
            return Response({"data": result_serializer.data}, status=200)
        except Season.DoesNotExist:
            return Response({"error": "Season does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class DeleteSeasonView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def delete(self, request, season_id):
        try:
            season = Season.objects.get(
                id=season_id,
                is_active=True
            )
            season.is_active=False
            season.save()
            
            return Response({"message": "Season deleted"}, status=200)
        except Season.DoesNotExist:
            return Response({"error": "Season does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class GetEpisodiesDataView(GenericAPIView):
    
    serializer_class = EpisodiesSerializer

    def get(self, request):
        try:
            episodies = Episodies.objects.filter(is_active=True)
            serializer = EpisodiesSerializer(episodies,many=True)
            return Response({"episodies": serializer.data}, status=200)
        except Episodies.DoesNotExist:
            return Response({"error": "Episodies does not exist"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

"""
class GetEpisodiesDataView(ListAPIView):
    permission_classes = None
    queryset = Episodies.objects.filter(is_active=True)
    serializer_class = EpisodiesSerializer
    filterset_class = EpisodiesFilter
"""

class GetEpisodieDataView(GenericAPIView):
    
    serializer_class = EpisodiesSerializer

    def get(self, request, episodie_id):
        try:
            episodies = Episodies.objects.filter(id=episodie_id,is_active=True)
            serializer = EpisodiesSerializer(episodies,many=True)
            return Response({"episodie": serializer.data}, status=200)
        except Episodies.DoesNotExist:
            return Response({"error": "Episodies does not exist"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CreateEpisodieView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateEpisodiesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        try:
            name = serializer.validated_data["name"]
            original_name = serializer.validated_data["original_name"]
            original_date = serializer.validated_data["original_date"]
            season_id = serializer.validated_data["season"]
            description = serializer.validated_data["description"]
            link1 = serializer.validated_data["link1"]
            link2 = serializer.validated_data["link2"]
            english = serializer.validated_data["english"]
            spoty = serializer.validated_data["spoty"]
            mediafire = serializer.validated_data["mediafire"]
            
            season = Season.objects.get(id=season_id)
            
            episodie = Episodies.objects.create(
                name=name,
                season=season,
                description=description,
                link1=link1,
                link2 = link2,
                english=english,
                spoty=spoty,
                mediafire = mediafire,
                original_name=original_name,
                original_date=original_date,
            )
            
            result_serializer = EpisodiesSerializer(episodie)
            
            return Response({"data": result_serializer.data}, status=200)
        except Season.DoesNotExist:
            return Response({"error": "Season does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class EditEpisodieView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditEpisodiesSerializer

    def post(self, request, episodie_id):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        try:
            name = serializer.validated_data["name"]
            season_id = serializer.validated_data["season"]
            original_name = serializer.validated_data["original_name"]
            original_date = serializer.validated_data["original_date"]
            description = serializer.validated_data["description"]
            link1 = serializer.validated_data["link1"]
            link2 = serializer.validated_data["link2"]
            english = serializer.validated_data["english"]
            spoty = serializer.validated_data["spoty"]
            mediafire = serializer.validated_data["mediafire"]
            
            episodie = Episodies.objects.get(id=episodie_id,is_active=True)
            
            if season_id:
                season = Season.objects.get(id=season_id)
                episodie.season=season
                
            if name:
                episodie.name=name
            
            if original_name:
                episodie.original_name = original_name
                
            if original_date:
                episodie.original_date = original_date
            
            if description:
                episodie.description =description
            
            if link1:
                episodie.link1=link1
                
            if link2:
                episodie.link2 = link2
            
            if english:
                episodie.english=english
            
            if spoty:
                episodie.spoty=spoty
            
            if mediafire:
                episodie.mediafire = mediafire
            
            episodie.save()
            
            result_serializer = EpisodiesSerializer(episodie)
            
            return Response({"data": result_serializer.data}, status=200)
        except Episodies.DoesNotExist:
            return Response({"error": "Episodies does not exist"}, status=404)
        except Season.DoesNotExist:
            return Response({"error": "Season does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DeleteEpisodieView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def delete(self, request, episodie_id):
        try:
            episodie = Episodies.objects.get(
                id=episodie_id,
                is_active=True)
            episodie.is_active=False
            episodie.save()
            return Response({"message": "Episodie deleted"}, status=200)
        except Episodies.DoesNotExist:
            return Response({"error": "Episodie does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
