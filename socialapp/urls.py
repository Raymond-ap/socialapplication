from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token
from .views import *

urlpatterns = [
    path('api-token-refresh/', refresh_jwt_token),
    path('login', Login, name="login")
]
