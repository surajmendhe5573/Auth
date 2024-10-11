from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,  LoginSerializer
from rest_framework.permissions import IsAuthenticated

# user registration view

class RegisterView(APIView):
    def post(self, request):
        serializer= RegisterSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User reistered successfully"}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer= LoginSerializer(data= request.data)
        if serializer.is_valid():
            username= serializer.validated_data['username']
            password= serializer.validated_data['password']
            user= authenticate(username=username, password=password)
            if user:
                refresh= RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }, status= status.HTTP_200_OK)
            return Response({"message": "Invalid Credentials"}, status= status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user= request.user
        user_data= {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        return Response({"message": "This is is protected view", "user": user_data})