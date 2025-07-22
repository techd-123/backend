from django.contrib import admin
from .models import *

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'capacity', 'location')
    list_filter = ('category',)
    search_fields = ('name', 'location')

class PlanningAndDecorAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class PhotographyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class MakeupAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class BridalWearAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'get_price_range')
    search_fields = ('name', 'location')
    list_filter = ('rating',)
    
    def get_price_range(self, obj):
        return f"₹{obj.price_range_min} - ₹{obj.price_range_max}"
    get_price_range.short_description = 'Price Range'

class GroomWearAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'get_price_range')
    search_fields = ('name', 'location')
    list_filter = ('rating',)
    
    def get_price_range(self, obj):
        return f"₹{obj.price_range_min} - ₹{obj.price_range_max}"
    get_price_range.short_description = 'Price Range'

class MehandiAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class WeddingCakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class CarRentalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class DJAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class JewelryRentalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class CateringAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price')
    search_fields = ('name', 'location')
    list_filter = ('rating',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    exclude = ['cart']

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_price')
    filter_horizontal = ('items',)  # This provides a better interface for ManyToMany
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('items')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'quantity', 'added_at', 'total_price')
    list_filter = ('content_type',)
    
    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_item_count')
    filter_horizontal = (
        'venues', 'planning_decor', 'photography', 'makeup',
        'bridal_wear', 'groom_wear', 'mehandi', 'wedding_cake'
    )
    
    def get_item_count(self, obj):
        count = 0
        for field in ['venues', 'planning_decor', 'photography', 'makeup',
                     'bridal_wear', 'groom_wear', 'mehandi', 'wedding_cake']:
            count += getattr(obj, field).count()
        return count
    get_item_count.short_description = 'Item Count'

# Register all models
admin.site.register(Venue, VenueAdmin)
admin.site.register(PlanningAndDecor, PlanningAndDecorAdmin)
admin.site.register(Photography, PhotographyAdmin)
admin.site.register(Makeup, MakeupAdmin)
admin.site.register(BridalWear, BridalWearAdmin)
admin.site.register(GroomWear, GroomWearAdmin)
admin.site.register(Mehandi, MehandiAdmin)
admin.site.register(WeddingCake, WeddingCakeAdmin)
admin.site.register(CarRental, CarRentalAdmin)
admin.site.register(DJ, DJAdmin)
admin.site.register(JewelryRental, JewelryRentalAdmin)
admin.site.register(Catering, CateringAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)