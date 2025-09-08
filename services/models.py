from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class BaseServiceModel(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_%(class)ss'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Common fields for all services
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='services/', null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and hasattr(self, '_state') and hasattr(self._state, 'user'):
            self.creator = self._state.user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.location}"

class Venue(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('premium', 'Premium'),
        ('budget_friendly', 'Budget Friendly'),
        ('popular', 'Popular'),
        ('luxury', 'Luxury'),
        ('outdoor', 'Outdoor'),
        ('indoor', 'Indoor'),
        ('beach', 'Beach'),
        ('garden', 'Garden'),
        ('banquet', 'Banquet Hall'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.category}) - {self.location}"

class PlanningAndDecor(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('full_planning', 'Full Wedding Planning'),
        ('partial_planning', 'Partial Planning'),
        ('day_coordination', 'Day-of Coordination'),
        ('decor_only', 'Decor Only'),
        ('theme_based', 'Theme Based'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    experience_years = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class Photography(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('pre_wedding', 'Pre-Wedding'),
        ('wedding_day', 'Wedding Day'),
        ('cinematography', 'Cinematography'),
        ('both', 'Photo + Video'),
        ('drone', 'Drone Photography'),
        ('traditional', 'Traditional'),
        ('candid', 'Candid'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    portfolio_link = models.URLField(blank=True, null=True)
    equipment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class Makeup(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('bridal', 'Bridal Makeup'),
        ('groom', 'Groom Makeup'),
        ('family', 'Family Makeup'),
        ('engagement', 'Engagement'),
        ('reception', 'Reception'),
        ('trial', 'Trial Session'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    brands_used = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class BridalWear(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('lehenga', 'Lehenga'),
        ('saree', 'Saree'),
        ('gown', 'Gown'),
        ('traditional', 'Traditional'),
        ('modern', 'Modern'),
        ('indo_western', 'Indo-Western'),
        ('custom', 'Custom Design'),
        ('rental', 'Rental'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2)
    fabric = models.CharField(max_length=100, blank=True, null=True)
    color_options = models.TextField(blank=True, null=True)
    
    def get_price_range(self):
        return f"₹{self.price_range_min} - ₹{self.price_range_max}"
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class GroomWear(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('sherwani', 'Sherwani'),
        ('suit', 'Suit'),
        ('traditional', 'Traditional'),
        ('modern', 'Modern'),
        ('indo_western', 'Indo-Western'),
        ('custom', 'Custom Design'),
        ('rental', 'Rental'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2)
    fabric = models.CharField(max_length=100, blank=True, null=True)
    
    def get_price_range(self):
        return f"₹{self.price_range_min} - ₹{self.price_range_max}"
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class Mehandi(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('bridal', 'Bridal Mehandi'),
        ('family', 'Family Mehandi'),
        ('simple', 'Simple Design'),
        ('intricate', 'Intricate Design'),
        ('arabic', 'Arabic Style'),
        ('indian', 'Indian Traditional'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    design_types = models.TextField(blank=True, null=True)
    duration_hours = models.PositiveIntegerField(default=2)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class WeddingCake(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('traditional', 'Traditional'),
        ('modern', 'Modern'),
        ('theme_based', 'Theme Based'),
        ('custom_design', 'Custom Design'),
        ('eggless', 'Eggless'),
        ('multiple_tier', 'Multiple Tier'),
        ('single_tier', 'Single Tier'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flavors = models.TextField(blank=True, null=True)
    serving_size = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class CarRental(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('luxury', 'Luxury Cars'),
        ('vintage', 'Vintage Cars'),
        ('suv', 'SUVs'),
        ('limousine', 'Limousine'),
        ('convertible', 'Convertible'),
        ('premium', 'Premium Sedan'),
        ('economic', 'Economic'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    car_model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.car_model} - {self.get_category_display()}"

class DJ(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('wedding', 'Wedding DJ'),
        ('reception', 'Reception DJ'),
        ('both', 'Wedding + Reception'),
        ('bollywood', 'Bollywood Specialist'),
        ('western', 'Western Music'),
        ('regional', 'Regional Music'),
        ('multilingual', 'Multilingual'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    music_genres = models.TextField(blank=True, null=True)
    equipment_provided = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class JewelryRental(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('bridal_set', 'Bridal Set'),
        ('necklace', 'Necklace'),
        ('earrings', 'Earrings'),
        ('bangles', 'Bangles'),
        ('maang_tikka', 'Maang Tikka'),
        ('nose_ring', 'Nose Ring'),
        ('complete_set', 'Complete Set'),
        ('traditional', 'Traditional'),
        ('modern', 'Modern'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=100, blank=True, null=True)
    stone_type = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class Catering(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('non_vegetarian', 'Non-Vegetarian'),
        ('both', 'Vegetarian + Non-Veg'),
        ('jain', 'Jain'),
        ('regional', 'Regional Cuisine'),
        ('international', 'International'),
        ('live_counters', 'Live Counters'),
        ('package', 'Package Deal'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price_per_plate = models.DecimalField(max_digits=10, decimal_places=2)
    min_guests = models.PositiveIntegerField(default=50)
    cuisine_types = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

# Wishlist and Cart models remain the same as your original
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venues = models.ManyToManyField(Venue, blank=True)
    planning_decor = models.ManyToManyField(PlanningAndDecor, blank=True)
    photography = models.ManyToManyField(Photography, blank=True)
    makeup = models.ManyToManyField(Makeup, blank=True)
    bridal_wear = models.ManyToManyField(BridalWear, blank=True)
    groom_wear = models.ManyToManyField(GroomWear, blank=True)
    mehandi = models.ManyToManyField(Mehandi, blank=True)
    wedding_cake = models.ManyToManyField(WeddingCake, blank=True)
    car_rentals = models.ManyToManyField(CarRental, blank=True)
    djs = models.ManyToManyField(DJ, blank=True)
    jewelry_rentals = models.ManyToManyField(JewelryRental, blank=True)
    catering = models.ManyToManyField(Catering, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Wishlist for {self.user.email}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.email}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    CONTENT_TYPE_CHOICES = [
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
    
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    object_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.content_type} (ID: {self.object_id})"
    
    def total_price(self):
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
        
        model_class = model_map.get(self.content_type)
        if not model_class:
            return 0
        
        try:
            obj = model_class.objects.get(pk=self.object_id)
            if hasattr(obj, 'price'):
                return obj.price * self.quantity
            elif hasattr(obj, 'price_range_min'):
                return obj.price_range_min * self.quantity
            elif hasattr(obj, 'price_per_plate'):
                return obj.price_per_plate * self.quantity
            return 0
        except model_class.DoesNotExist:
            return 0