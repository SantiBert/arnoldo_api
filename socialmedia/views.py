from django.core.exceptions import PermissionDenied

from rest_framework import permissions
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import (
    SocialMedia, 
    EnlaceSocial,
    )

from .serializer import (
    SocialMediaSerilizer,
    SocialMediaCreateSerilizer,
    SocialMediaEditSerilizer,
)

class GetSocialMediaDataView(GenericAPIView):
    
    serializer_class = SocialMediaSerilizer

    def get(self, request):
        try:
            episodies = SocialMedia.objects.all()
            serializer = SocialMediaSerilizer(episodies,many=True)
            return Response({"episodies": serializer.data}, status=200)
        except SocialMedia.DoesNotExist:
            return Response({"error": "Episodies does not exist"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

"""
class GetSocialMediaDataView(ListAPIView):
    permission_classes = None
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerilizer
    #filterset_class = EpisodiesFilter
"""

class CreateSocialMediaView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialMediaCreateSerilizer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        try:
            name = serializer.validated_data["name"]
            icon = serializer.validated_data["icon"]
            link = serializer.validated_data["link"]
            
            social_media = SocialMedia.objects.create(
                name=name,
                icon=icon
            )
            enlase_social = EnlaceSocial.objects.create(
                social_media = social_media,
                link = link
            )
            
            result_serializer = SocialMediaSerilizer(social_media)
            
            return Response({"data": result_serializer.data}, status=200)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class EditSocialMediaView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialMediaEditSerilizer

    def post(self, request, social_media_id):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        try:
            name = serializer.validated_data["name"]
            icon = serializer.validated_data["icon"]
            link = serializer.validated_data["link"]
            
            social_media = SocialMedia.objects.get(id=social_media_id)
            
            enlase_social = EnlaceSocial.objects.get(
                social_media = social_media
            )
            
            if name:
                social_media.name = name
            
            if icon:
                social_media.icon = icon
                
            if link:
                enlase_social.link = link
                
            social_media.save()
            enlase_social.save()
            
            result_serializer = SocialMediaSerilizer(social_media)
            
            return Response({"data": result_serializer.data}, status=200)
        except SocialMedia.DoesNotExist:
            return Response({"error": "Social media does not exist"}, status=404)
        except EnlaceSocial.DoesNotExist:
            return Response({"error": "Enlace Social does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class DeleteSocialMediaView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def delete(self, request, social_media_id):
        try:
            social_media = SocialMedia.objects.get(id=social_media_id)
            
            enlase_social = EnlaceSocial.objects.get(
                social_media = social_media
            ).delete()
            
            social_media.delete()
            
            return Response({"message": "Social media deleted"}, status=200)
        except SocialMedia.DoesNotExist:
            return Response({"error": "Social media does not exist"}, status=404)
        except EnlaceSocial.DoesNotExist:
            return Response({"error": "Enlace Social does not exist"}, status=404)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)