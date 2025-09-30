from django.urls import path
from .views import *

urlpatterns = [
    # Venues
    path('venues/', VenueListView.as_view(), name='venue-list'),
    path('venues/create/', VenueCreateView.as_view(), name='venue-create'),
    path('venues/<int:pk>/', VenueDetailView.as_view(), name='venue-detail'),
    
    # Planning & Decor
    path('planning-decor/', PlanningAndDecorListView.as_view(), name='planning-decor-list'),
    path('planning-decor/create/', PlanningAndDecorCreateView.as_view(), name='planning-decor-create'),
    path('planning-decor/<int:pk>/', PlanningAndDecorDetailView.as_view(), name='planning-decor-detail'),
    
    # Photography
    path('photography/', PhotographyListView.as_view(), name='photography-list'),
    path('photography/create/', PhotographyCreateView.as_view(), name='photography-create'),
    path('photography/<int:pk>/', PhotographyDetailView.as_view(), name='photography-detail'),
    
    # Makeup
    path('makeup/', MakeupListView.as_view(), name='makeup-list'),
    path('makeup/create/', MakeupCreateView.as_view(), name='makeup-create'),
    path('makeup/<int:pk>/', MakeupDetailView.as_view(), name='makeup-detail'),
    
    # Bridal Wear
    path('bridal-wear/', BridalWearListView.as_view(), name='bridal-wear-list'),
    path('bridal-wear/create/', BridalWearCreateView.as_view(), name='bridal-wear-create'),
    path('bridal-wear/<int:pk>/', BridalWearDetailView.as_view(), name='bridal-wear-detail'),
    
    # Groom Wear
    path('groom-wear/', GroomWearListView.as_view(), name='groom-wear-list'),
    path('groom-wear/create/', GroomWearCreateView.as_view(), name='groom-wear-create'),
    path('groom-wear/<int:pk>/', GroomWearDetailView.as_view(), name='groom-wear-detail'),
    
    # Mehandi
    path('mehandi/', MehandiListView.as_view(), name='mehandi-list'),
    path('mehandi/create/', MehandiCreateView.as_view(), name='mehandi-create'),
    path('mehandi/<int:pk>/', MehandiDetailView.as_view(), name='mehandi-detail'),
    
    # Wedding Cake
    path('wedding-cake/', WeddingCakeListView.as_view(), name='wedding-cake-list'),
    path('wedding-cake/create/', WeddingCakeCreateView.as_view(), name='wedding-cake-create'),
    path('wedding-cake/<int:pk>/', WeddingCakeDetailView.as_view(), name='wedding-cake-detail'),

    # Car Rental
    path('car-rentals/', CarRentalListView.as_view(), name='car-rental-list'),
    path('car-rentals/create/', CarRentalCreateView.as_view(), name='car-rental-create'),
    path('car-rentals/<int:pk>/', CarRentalDetailView.as_view(), name='car-rental-detail'),
    
    # DJ
    path('djs/', DJListView.as_view(), name='dj-list'),
    path('djs/create/', DJCreateView.as_view(), name='dj-create'),
    path('djs/<int:pk>/', DJDetailView.as_view(), name='dj-detail'),
    
    # Jewelry Rental
    path('jewelry-rentals/', JewelryRentalListView.as_view(), name='jewelry-rental-list'),
    path('jewelry-rentals/create/', JewelryRentalCreateView.as_view(), name='jewelry-rental-create'),
    path('jewelry-rentals/<int:pk>/', JewelryRentalDetailView.as_view(), name='jewelry-rental-detail'),
    
    # Catering
    path('catering/', CateringListView.as_view(), name='catering-list'),
    path('catering/create/', CateringCreateView.as_view(), name='catering-create'),
    path('catering/<int:pk>/', CateringDetailView.as_view(), name='catering-detail'),

    # Cart URLs
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/<int:item_id>/', CartItemView.as_view(), name='cart-item-detail'),
    path('cart/checkout/', CartCheckoutView.as_view(), name='cart-checkout'),
    
    # Wishlist URLs
    path('wishlist/', WishlistView.as_view(), name='wishlist'),

    # Global Search:
    path('search/', GlobalSearchView.as_view(), name='global-search'),
]