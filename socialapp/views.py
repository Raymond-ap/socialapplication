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
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_jwt.settings import api_settings
import jwt
from .serializers import *
from django.conf import settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLE


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


@csrf_exempt
@api_view(['POST'])
def Login(request):

    email = request.data['email']
    password = request.data['password']

    try:
        user = get_or_none(User, email=email)
        if not user:
            return Response({'error': 'No account found for this user'}, status=status.HTTP_401_UNAUTHORIZED)
        is_active = user.is_active
        if not is_active:
            return Response({'error': 'User account is deactivated'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if check_password(password, user.password):
                try:

                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    serializer = UserSerializer(user)

                    resp = {
                        'token': token,
                        'user': serializer.data
                    }

                    return Response(resp, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'error': 'Wrong email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Wrong email or password'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_403_FORBIDDEN)
