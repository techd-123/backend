from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, OTP
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from knox.models import AuthToken

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password', 'token']
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False}
        }
    
    def get_token(self, obj):
        return AuthToken.objects.create(user=obj)[1]
    
    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("Either email or phone number must be provided")
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class OTPVerifySerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    otp_type = serializers.ChoiceField(choices=[('email', 'Email'), ('phone', 'Phone')])

class ResendOTPSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    otp_type = serializers.ChoiceField(choices=[('email', 'Email'), ('phone', 'Phone')])

class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField()
    token = serializers.SerializerMethodField()
    
    def get_token(self, obj):
        return AuthToken.objects.create(user=obj)[1]
    
    def validate(self, data):
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')
        
        if '@' in email_or_phone:
            try:
                user = CustomUser.objects.get(email=email_or_phone)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            try:
                user = CustomUser.objects.get(phone_number=email_or_phone)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials.")
        
        if not user.is_active:
            pending_verifications = []
            if user.email and not user.is_email_verified:
                pending_verifications.append('email')
            if user.phone_number and not user.is_phone_verified:
                pending_verifications.append('phone')
            
            raise serializers.ValidationError({
                'error': 'Account not verified.',
                'pending_verifications': pending_verifications,
                'user_id': user.id
            })
        
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 
                'is_email_verified', 'is_phone_verified', 'is_active']