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
    list_display = ['user', 'created_at', 'updated_at']
    filter_horizontal = ['items']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'quantity', 'added_at']
    list_filter = ['content_type', 'added_at']