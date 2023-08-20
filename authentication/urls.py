from django.urls import path, include
from .views import *




urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/register', RegisterView.as_view(), name="register"),
    path('auth/update-profile', update_profile, name="update_profile"),
]
