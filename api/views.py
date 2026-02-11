from  rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import SailorUser
from .serializers import SailorUserSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import authenticate
from .otpgenerstor import generate_otp
from django.utils import timezone
from datetime import timedelta

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("id_token")

        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            "404596195032-7qe88v9d7soicdvmkt640i497e838gah.apps.googleusercontent.com"
        )

        email = idinfo["email"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email}
        )

   
        SailorUser.objects.get_or_create(email=user)
        sailor_user = SailorUser.objects.get(email=user)
        print(sailor_user)
        sailor_user.is_google_auth = True
        sailor_user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

class sailoruserlistview(generics.ListCreateAPIView):
    queryset = SailorUser.objects.all()
    serializer_class = SailorUserSerializer
    permission_classes = [AllowAny]
    
# Sign up User View
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.save()
        sailor_user = SailorUser.objects.create(email=user)
        sailor_user.otp = generate_otp()
        
        sailor_user.otp_created_at = timezone.now()
        sailor_user.save()
        send_mail(
            subject="Verify Your Otp",
            message=f"Your otp is {sailor_user.otp}", 
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[sailor_user.email.email],
            fail_silently=False
        )
        

        return Response(
            {'message': 'User created successfully. Please verify your email.'},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print(e)
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

#Normal Login View
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        sailor_obj = SailorUser.objects.get(email=user)
    
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'email': user.email,
                'name': sailor_obj.name,
            }
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    print(email)
    try:
        user = User.objects.get(email=email)
        sailor_user = SailorUser.objects.get(email=user)
    except User.DoesNotExist  :
        return 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    except SailorUser.DoesNotExist:
        return Response({"msg":"User Not Found "},status=404)
    
    if sailor_user.otp != otp:
        return Response({"msg":"Invalid OTP"},status=400)
    
    if timezone.now() > sailor_user.otp_created_at + timedelta(minutes=5):
        return Response({"msg":"OTP expired"},status=400)

    sailor_user.is_verified = True
    sailor_user.otp = None
    sailor_user.save()
    
    return Response({"message":"Email verfied Successfully"})
  
