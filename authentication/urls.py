from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView




urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/register', RegisterView.as_view(), name="register"),
    path('auth/update-profile', update_profile, name="update_profile"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
