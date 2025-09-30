# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LogoutAllView as KnoxLogoutAllView
from knox.models import AuthToken
from django.contrib.auth import login, authenticate
from .models import *
from .serializers import *
from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail
from .sms_utils import send_sms_otp
from django.conf import settings
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            verification_methods = []
            if user.email:
                verification_methods.append('email')
            if user.phone_number:
                verification_methods.append('phone')
            
            for method in verification_methods:
                otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
                
                OTP.objects.create(
                    user=user,
                    otp=otp_code,
                    otp_type=method,
                    expires_at=expires_at
                )
                
                if method == 'email':
                    send_mail(
                        'Verify Your Account',
                        f'Your verification code is {otp_code}. Valid for {settings.OTP_EXPIRY_MINUTES} minutes.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                else:
                    if not send_sms_otp(user.phone_number, otp_code):
                        OTP.objects.filter(user=user, otp_type=method, otp=otp_code).delete()
                        verification_methods.remove('phone')
                        continue
            
            response_data = {
                'message': 'Registration successful. Please verify your account.',
                'user_id': user.id,
                'verification_methods': verification_methods,
            }
            
            if user.email:
                response_data['email'] = user.email
            if user.phone_number and 'phone' in verification_methods:
                response_data['phone_number'] = user.phone_number
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data['email_or_phone']
            otp_code = serializer.validated_data['otp']
            otp_type = serializer.validated_data['otp_type']
            
            try:
                if otp_type == 'email':
                    user = CustomUser.objects.get(email=email_or_phone)
                else:
                    user = CustomUser.objects.get(phone_number=email_or_phone)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                otp = OTP.objects.get(
                    user=user,
                    otp=otp_code,
                    otp_type=otp_type,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
            except OTP.DoesNotExist:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            
            otp.is_used = True
            otp.save()
            
            if otp_type == 'email':
                user.is_email_verified = True
            else:
                user.is_phone_verified = True
            
            required_verifications = []
            if user.email:
                required_verifications.append('email')
            if user.phone_number:
                required_verifications.append('phone')
            
            all_verified = all([
                user.is_email_verified if 'email' in required_verifications else True,
                user.is_phone_verified if 'phone' in required_verifications else True
            ])
            
            if all_verified:
                user.is_active = True
                user.save()
                
                
                return Response({
                    'message': 'Account verification complete! Please login to continue.',
                    'user_id': user.id,
                    'is_active': True
                }, status=status.HTTP_200_OK)
            else:
                user.save()
                pending_verifications = [
                    method for method in required_verifications 
                    if (method == 'email' and not user.is_email_verified) or 
                       (method == 'phone' and not user.is_phone_verified)
                ]
                return Response({
                    'message': f'{otp_type.capitalize()} verified successfully.',
                    'pending_verifications': pending_verifications,
                    'is_active': False
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data['email_or_phone']
            otp_type = serializer.validated_data['otp_type']
            
            try:
                if otp_type == 'email':
                    user = CustomUser.objects.get(email=email_or_phone)
                else:
                    user = CustomUser.objects.get(phone_number=email_or_phone)
            except CustomUser.DoesNotExist:
                return Response({'error': f'User with this {otp_type} does not exist.'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            if (otp_type == 'email' and user.is_email_verified) or \
               (otp_type == 'phone' and user.is_phone_verified):
                return Response({
                    'error': f'Your {otp_type} is already verified.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            last_otp = OTP.objects.filter(
                user=user,
                otp_type=otp_type
            ).order_by('-created_at').first()
            
            if last_otp and (timezone.now() - last_otp.created_at).seconds < settings.OTP_RESEND_COOLDOWN:
                time_remaining = settings.OTP_RESEND_COOLDOWN - (timezone.now() - last_otp.created_at).seconds
                return Response({
                    'error': f'Please wait {time_remaining} seconds before requesting a new OTP.'
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            
            OTP.objects.create(
                user=user,
                otp=otp_code,
                otp_type=otp_type,
                expires_at=expires_at
            )
            
            if otp_type == 'email':
                send_mail(
                    'Your New Verification Code',
                    f'Your new verification code is {otp_code}. Valid for {settings.OTP_EXPIRY_MINUTES} minutes.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            else:
                if not send_sms_otp(user.phone_number, otp_code):
                    return Response({'error': 'Failed to send SMS OTP. Please try again.'}, 
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'message': f'New OTP sent to your {otp_type}.',
                'next_resend_available_after': settings.OTP_RESEND_COOLDOWN
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Check if user is active (all verifications completed)
            if not user.is_active:
                return Response({
                    'error': 'Account not verified. Please complete verification process.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            login(request, user)
            
            # Get the token from Knox (this is where token gets created)
            response = super().post(request, format=None)
            
            # Add user info to response
            if response.status_code == status.HTTP_200_OK:
                response.data.update({
                    'user_id': user.id,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'is_email_verified': user.is_email_verified,
                    'is_phone_verified': user.is_phone_verified
                })
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(KnoxLogoutView):
    permission_classes = [permissions.IsAuthenticated]

class LogoutAllView(KnoxLogoutAllView):
    permission_classes = [permissions.IsAuthenticated]