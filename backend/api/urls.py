
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import api_home
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    TokenObtainPairView
)
urlpatterns = [
    

    path('auth/',obtain_auth_token),
    path('token/',TokenObtainPairView.as_view(),name='token_obatin_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('token/',TokenVerifyView.as_view(),name='token_verify'),
    
    path('',api_home), #Local host:8000
]
    

