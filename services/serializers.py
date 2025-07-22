from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = fields

class BaseServiceSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    
    class Meta:
        fields = '__all__'
        read_only_fields = ['creator', 'created_at', 'updated_at']

class VenueSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = Venue

class PlanningAndDecorSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = PlanningAndDecor

class PhotographySerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = Photography

class MakeupSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = Makeup

class BridalWearSerializer(BaseServiceSerializer):
    price_range = serializers.SerializerMethodField()
    
    class Meta(BaseServiceSerializer.Meta):
        model = BridalWear
    
    def get_price_range(self, obj):
        return f"₹{obj.price_range_min} - ₹{obj.price_range_max}"

class GroomWearSerializer(BaseServiceSerializer):
    price_range = serializers.SerializerMethodField()
    
    class Meta(BaseServiceSerializer.Meta):
        model = GroomWear
    
    def get_price_range(self, obj):
        return f"₹{obj.price_range_min} - ₹{obj.price_range_max}"

class MehandiSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = Mehandi

class WeddingCakeSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = WeddingCake

class CarRentalSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = CarRental

class DJSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = DJ

class JewelryRentalSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = JewelryRental

class CateringSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = Catering

class CartItemSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'content_type', 'object_id', 'quantity', 'added_at', 'item_details', 'total_price']
    
    def get_item_details(self, obj):
        model_map = {
            'venue': (Venue, VenueSerializer),
            'planning_decor': (PlanningAndDecor, PlanningAndDecorSerializer),
            'photography': (Photography, PhotographySerializer),
            'makeup': (Makeup, MakeupSerializer),
            'bridal_wear': (BridalWear, BridalWearSerializer),
            'groom_wear': (GroomWear, GroomWearSerializer),
            'mehandi': (Mehandi, MehandiSerializer),
            'wedding_cake': (WeddingCake, WeddingCakeSerializer),
            'car_rental': (CarRental, CarRentalSerializer),
            'dj': (DJ, DJSerializer),
            'jewelry_rental': (JewelryRental, JewelryRentalSerializer),
            'catering': (Catering, CateringSerializer),
        }
        
        model_class, serializer_class = model_map.get(obj.content_type, (None, None))
        if not model_class:
            return None
        
        try:
            item = model_class.objects.get(pk=obj.object_id)
            return serializer_class(item).data
        except model_class.DoesNotExist:
            return None
    
    def get_total_price(self, obj):
        return obj.total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = CreatorSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at', 'total_price']
    
    def get_total_price(self, obj):
        return obj.total_price()

class WishlistSerializer(serializers.ModelSerializer):
    venues = VenueSerializer(many=True, read_only=True)
    planning_decor = PlanningAndDecorSerializer(many=True, read_only=True)
    photography = PhotographySerializer(many=True, read_only=True)
    makeup = MakeupSerializer(many=True, read_only=True)
    bridal_wear = BridalWearSerializer(many=True, read_only=True)
    groom_wear = GroomWearSerializer(many=True, read_only=True)
    mehandi = MehandiSerializer(many=True, read_only=True)
    wedding_cake = WeddingCakeSerializer(many=True, read_only=True)
    user = CreatorSerializer(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'venues', 'planning_decor', 'photography', 
                 'makeup', 'bridal_wear', 'groom_wear', 'mehandi', 
                 'wedding_cake', 'created_at']