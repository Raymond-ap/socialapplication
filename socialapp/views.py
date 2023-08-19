from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, generics
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes, throttle_classes
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from rest_framework.views import APIView
from .utils import *
from django.contrib.auth import get_user_model



class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Custom validation logic
        email = serializer.validated_data['email']
        if get_user_model().objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # If validation passes, save the user
        user = serializer.save()
        
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request=self.request, email=email, password=password)

        if user is None:
            return Response({'error': 'No account found for this user.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        is_active = user.is_active
        if not is_active:
            return Response({'error': 'User account is deactivated'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)
