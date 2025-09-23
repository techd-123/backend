from django.contrib import admin
from .models import *

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(PlanningAndDecor)
class PlanningAndDecorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(Photography)
class PhotographyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(Makeup)
class MakeupAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(BridalWear)
class BridalWearAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price_range_min', 'price_range_max', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(GroomWear)
class GroomWearAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price_range_min', 'price_range_max', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(Mehandi)
class MehandiAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(WeddingCake)
class WeddingCakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(CarRental)
class CarRentalAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location', 'car_model']

@admin.register(DJ)
class DJAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(JewelryRental)
class JewelryRentalAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price', 'rating', 'creator']
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location']

@admin.register(Catering)
class CateringAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price_per_plate', 'rating', 'creator']  # Changed 'price' to 'price_per_plate'
    list_filter = ['category', 'location', 'rating']
    search_fields = ['name', 'location', 'cuisine_types']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    filter_horizontal = [
        'venues', 'planning_decor', 'photography', 'makeup', 
        'bridal_wear', 'groom_wear', 'mehandi', 'wedding_cake',
        'car_rentals', 'djs', 'jewelry_rentals', 'catering'
    ]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'total_price', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def item_count(self, obj):
        return obj.item_count()
    item_count.short_description = 'Items'
    
    def total_price(self, obj):
        return f"₹{obj.total_price()}"
    total_price.short_description = 'Total'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'quantity', 'total_price', 'added_at']
    list_filter = ['content_type', 'added_at']
    readonly_fields = ['added_at']
    
    def user(self, obj):
        return obj.cart_set.first().user if obj.cart_set.exists() else 'No user'
    
    def total_price(self, obj):
        return f"₹{obj.total_price()}"
    total_price.short_description = 'Total Price'