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

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and hasattr(self, '_state') and hasattr(self._state, 'user'):
            self.creator = self._state.user
        super().save(*args, **kwargs)

class Venue(BaseServiceModel):
    CATEGORY_CHOICES = [
        ('premium', 'Premium'),
        ('budget friendly', 'Budget Friendly'),
        ('popular', 'Popular'),
        ('luxury', 'Luxury'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='venues/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.category}) - {self.location}"

class PlanningAndDecor(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='planning_decor/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - Rating: {self.rating}"

class Photography(BaseServiceModel):
    name = models.CharField(max_length=100)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photography/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class Makeup(BaseServiceModel):
    name = models.CharField(max_length=100)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='makeup/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - Rating: {self.rating}"

class BridalWear(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bridal_wear/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_price_range()}"

    def get_price_range(self):
        return f"₹{self.price_range_min} - ₹{self.price_range_max}"

class GroomWear(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='groom_wear/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_price_range()}"

    def get_price_range(self):
        return f"₹{self.price_range_min} - ₹{self.price_range_max}"

class Mehandi(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='mehandi/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - Rating: {self.rating}"

class WeddingCake(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='wedding_cakes/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - Rating: {self.rating}"
    
class CarRental(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_rentals/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class DJ(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='djs/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - Rating: {self.rating}"

class JewelryRental(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='jewelry_rentals/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class Catering(BaseServiceModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='catering/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - Rating: {self.rating}"

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
            return 0
        except model_class.DoesNotExist:
            return 0