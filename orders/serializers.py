from rest_framework import serializers
from .models import Order, OrderItem, VendorOrderNotification
from services.serializers import (
    VenueSerializer, PlanningAndDecorSerializer, PhotographySerializer, 
    MakeupSerializer, BridalWearSerializer, GroomWearSerializer,
    MehandiSerializer, WeddingCakeSerializer, CarRentalSerializer,
    DJSerializer, JewelryRentalSerializer, CateringSerializer
)

class OrderItemSerializer(serializers.ModelSerializer):
    service_details = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'service_type', 'service_id', 'service_name', 
            'service_price', 'vendor_name', 'vendor_email', 'quantity',
            'unit_price', 'total_price', 'service_date', 'service_time',
            'notes', 'service_details'
        ]
        read_only_fields = ['service_name', 'service_price', 'vendor_name', 'vendor_email']
    
    def get_service_details(self, obj):
        """Get detailed service information"""
        model_serializer_map = {
            'venue': VenueSerializer,
            'planning_decor': PlanningAndDecorSerializer,
            'photography': PhotographySerializer,
            'makeup': MakeupSerializer,
            'bridal_wear': BridalWearSerializer,
            'groom_wear': GroomWearSerializer,
            'mehandi': MehandiSerializer,
            'wedding_cake': WeddingCakeSerializer,
            'car_rental': CarRentalSerializer,
            'dj': DJSerializer,
            'jewelry_rental': JewelryRentalSerializer,
            'catering': CateringSerializer,
        }
        
        serializer_class = model_serializer_map.get(obj.service_type)
        if serializer_class and obj.content_object:
            return serializer_class(obj.content_object).data
        return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_details', 'customer_name',
            'customer_email', 'customer_phone', 'total_amount', 'order_status',
            'payment_status', 'event_date', 'special_instructions', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'created_at', 'updated_at']
    
    def get_customer_details(self, obj):
        from accounts.serializers import UserSerializer
        return UserSerializer(obj.customer).data

class CreateOrderItemSerializer(serializers.Serializer):
    service_type = serializers.ChoiceField(choices=OrderItem.SERVICE_TYPE_CHOICES)
    service_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)
    service_date = serializers.DateField(required=False, allow_null=True)
    service_time = serializers.TimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)
    event_date = serializers.DateField(required=False, allow_null=True)
    special_instructions = serializers.CharField(required=False, allow_blank=True)
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required")
        return value

class VendorOrderNotificationSerializer(serializers.ModelSerializer):
    order_details = OrderSerializer(source='order', read_only=True)
    
    class Meta:
        model = VendorOrderNotification
        fields = [
            'id', 'order', 'order_details', 'email_sent', 'email_sent_at',
            'viewed', 'viewed_at', 'created_at'
        ]
        read_only_fields = fields

class UpdateOrderStatusSerializer(serializers.Serializer):
    order_status = serializers.ChoiceField(
        choices=Order.ORDER_STATUS_CHOICES, 
        required=False
    )
    payment_status = serializers.ChoiceField(
        choices=Order.PAYMENT_STATUS_CHOICES, 
        required=False
    )
    
    def validate(self, data):
        if not data:
            raise serializers.ValidationError("At least one status must be provided")
        return data