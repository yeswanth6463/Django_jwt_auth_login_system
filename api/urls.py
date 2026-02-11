from django.contrib import admin
from django.urls import path 
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView






urlpatterns = [
     path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('google-login/',views.GoogleLoginView.as_view(), name='google-login'),
    path('userlist/',views.sailoruserlistview.as_view(),name='userlist'),
    path('register/',views.signup_user,name = 'signup user'),
    path('loginuser/',views.login_user,name = 'login user'),
    path('verify/',views.verify_email,name = "verify email"),

]

