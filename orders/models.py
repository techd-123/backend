from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from services.models import (
    Venue, PlanningAndDecor, Photography, Makeup, BridalWear, GroomWear,
    Mehandi, WeddingCake, CarRental, DJ, JewelryRental, Catering
)

User = get_user_model()

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Customer Information
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    
    # Order Details
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Status
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_date = models.DateField(null=True, blank=True)
    
    # Additional Information
    special_instructions = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        import random
        import string
        from django.utils import timezone
        
        timestamp = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.digits, k=6))
        return f"ORD{timestamp}{random_str}"
    
    def get_vendors(self):
        """Get all vendors associated with this order"""
        vendors = set()
        for item in self.items.all():
            if hasattr(item.content_object, 'creator') and item.content_object.creator:
                vendors.add(item.content_object.creator)
        return list(vendors)

class OrderItem(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('venue', 'Venue'),
        ('planning_decor', 'Planning & Decor'),
        ('photography', 'Photography'),
        ('makeup', 'Makeup'),
        ('bridal_wear', 'Bridal Wear'),
        ('groom_wear', 'Groom Wear'),
        ('mehandi', 'Mehandi'),
        ('wedding_cake', 'Wedding Cake'),
        ('car_rental', 'Car Rental'),
        ('dj', 'DJ'),
        ('jewelry_rental', 'Jewelry Rental'),
        ('catering', 'Catering'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    # Service Type and Reference
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    service_id = models.PositiveIntegerField()
    
    # Service Details (cached at time of order)
    service_name = models.CharField(max_length=255)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_name = models.CharField(max_length=255)
    vendor_email = models.EmailField()
    
    # Quantity and Pricing
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Service-specific details
    service_date = models.DateField(null=True, blank=True)
    service_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.quantity} x {self.service_name} (Order #{self.order.order_number})"
    
    @property
    def content_object(self):
        """Get the actual service object"""
        model_map = {
            'venue': Venue,
            'planning_decor': PlanningAndDecor,
            'photography': Photography,
            'makeup': Makeup,
            'bridal_wear': BridalWear,
            'groom_wear': GroomWear,
            'mehandi': Mehandi,
            'wedding_cake': WeddingCake,
            'car_rental': CarRental,
            'dj': DJ,
            'jewelry_rental': JewelryRental,
            'catering': Catering,
        }
        
        model_class = model_map.get(self.service_type)
        if model_class:
            try:
                return model_class.objects.get(pk=self.service_id)
            except model_class.DoesNotExist:
                return None
        return None
    
    def save(self, *args, **kwargs):
        # Calculate total price before saving
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class VendorOrderNotification(models.Model):
    """Track which vendors have been notified about orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_notifications')
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['order', 'vendor']
    
    def __str__(self):
        return f"Notification for {self.vendor.email} - Order #{self.order.order_number}"