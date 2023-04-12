from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from django.contrib.auth import authenticate

from .models import CustomUser
from .serializer import CustomUserSerializer, CustomRegisterSerializer, CustomLoginSerializer


class CustomUserView(GenericAPIView):
    
    serializer_class = CustomUserSerializer
    
    def get(self, request):
        users = CustomUser.objects.filter(is_active=True)
        serializer = CustomUserSerializer(users, many=True)
        return Response({"data": serializer.data}, status=200)

class CustomRegisterView(GenericAPIView):
    
    serializer_class = CustomRegisterSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        
        try:
            user = serializer.save()
            
            token = Token.objects.create(user=user)
            json = serializer.data
            json['token'] = token.key
            return Response(json, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
class LoginView(GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        try:
            nickname = serializer.validated_data['nickname']
            password = serializer.validated_data['password']
            user = authenticate(username=nickname, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=200)
            else:
                return Response({'error': 'Usuario o contraseña incorrectos'}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=500)