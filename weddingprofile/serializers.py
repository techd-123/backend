# weddingprofile/serializers.py
from rest_framework import serializers
from .models import WeddingProfile
from django.utils import timezone

class WeddingProfileSerializer(serializers.ModelSerializer):
    partner_details = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = WeddingProfile
        fields = [
            'id', 'owner', 'partner', 'bride', 'groom', 'religion', 'caste',
            'wedding_date', 'engagement_date', 'reception_date',
            'wedding_venue', 'engagement_venue', 'reception_venue',
            'partner_can_edit', 'created_at', 'updated_at',
            'partner_details', 'can_edit'
        ]
        read_only_fields = ('owner', 'created_at', 'updated_at')

    def get_partner_details(self, obj):
        if obj.partner:
            return {
                'id': obj.partner.id,
                'email': obj.partner.email,
                'phone': obj.partner.phone_number
            }
        return None

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            return user == obj.owner or (user == obj.partner and obj.partner_can_edit)
        return False
    
    def validate_partner(self, value):
        if value:
            if value == self.context['request'].user:
                raise serializers.ValidationError("You cannot set yourself as partner")
        return value
    
    def validate(self, data):
        # Validate engagement date is before wedding date if both exist
        engagement_date = data.get('engagement_date')
        wedding_date = data.get('wedding_date')
        if engagement_date and wedding_date and engagement_date >= wedding_date:
            raise serializers.ValidationError(
                {"engagement_date": "Engagement date must be before wedding date"}
            )
        # Validate wedding date is in the future
        if wedding_date and wedding_date < timezone.now().date():
            raise serializers.ValidationError(
                {"wedding_date" : "Wedding date must be in the future"}
            )
        return data