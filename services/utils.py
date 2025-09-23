from django.core.cache import cache

def get_user_cart(user):
    """Get or create user cart with caching"""
    cache_key = f"user_cart_{user.id}"
    cart = cache.get(cache_key)
    
    if not cart:
        cart, created = Cart.objects.get_or_create(user=user)
        # Cache for 1 hour
        cache.set(cache_key, cart, 3600)
    
    return cart

def clear_cart_cache(user):
    """Clear cart cache"""
    cache_key = f"user_cart_{user.id}"
    cache.delete(cache_key)