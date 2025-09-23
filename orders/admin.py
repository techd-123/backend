from django.contrib import admin
from .models import Order, OrderItem, VendorOrderNotification

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['service_name', 'service_price', 'vendor_name', 'unit_price', 'total_price']

class VendorNotificationInline(admin.TabularInline):
    model = VendorOrderNotification
    extra = 0
    readonly_fields = ['vendor', 'email_sent', 'email_sent_at', 'viewed', 'viewed_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'customer_email', 'total_amount', 
                   'order_status', 'payment_status', 'created_at']
    list_filter = ['order_status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline, VendorNotificationInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'total_amount')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Status', {
            'fields': ('order_status', 'payment_status')
        }),
        ('Event Details', {
            'fields': ('event_date', 'special_instructions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'service_name', 'service_type', 'quantity', 'unit_price', 'total_price']
    list_filter = ['service_type', 'order__order_status']
    search_fields = ['service_name', 'order__order_number']
    readonly_fields = ['service_name', 'service_price', 'vendor_name', 'unit_price', 'total_price']

@admin.register(VendorOrderNotification)
class VendorOrderNotificationAdmin(admin.ModelAdmin):
    list_display = ['order', 'vendor', 'email_sent', 'email_sent_at', 'viewed', 'viewed_at']
    list_filter = ['email_sent', 'viewed', 'created_at']
    readonly_fields = ['order', 'vendor', 'created_at']