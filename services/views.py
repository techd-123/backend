from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
from .permissions import IsStaffOrCreatorOrReadOnly

User = get_user_model()

class ServiceListView(APIView):
    """Base list view for all services with filtering capabilities"""
    permission_classes = [AllowAny]  # Anyone can view
    model = None
    serializer_class = None
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        
        # Filter by category if provided
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        # Filter by creator if provided
        creator_id = self.request.query_params.get('creator')
        if creator_id:
            queryset = queryset.filter(creator__id=creator_id)
            
        # Filter by location if provided
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        # Filter by name/search term if provided
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        # Filter by price range if provided
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            # Handle both price and price_range_min fields
            price_field = 'price' if hasattr(self.model, 'price') else 'price_range_min'
            queryset = queryset.filter(**{f'{price_field}__gte': min_price})
            
        if max_price:
            price_field = 'price' if hasattr(self.model, 'price') else 'price_range_max'
            queryset = queryset.filter(**{f'{price_field}__lte': max_price})
            
        # Filter by rating if provided
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
            
        return queryset
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class ServiceDetailView(APIView):
    """Base detail view for all services with CRUD operations"""
    permission_classes = [IsStaffOrCreatorOrReadOnly]
    model = None
    serializer_class = None
    
    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
    
    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)
    
    def post(self, request):
        # Store user in model state to be set as creator during save
        self.model._state.user = request.user
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Concrete service views
class VenueListView(ServiceListView):
    model = Venue
    serializer_class = VenueSerializer

class VenueDetailView(ServiceDetailView):
    model = Venue
    serializer_class = VenueSerializer

class PlanningAndDecorListView(ServiceListView):
    model = PlanningAndDecor
    serializer_class = PlanningAndDecorSerializer

class PlanningAndDecorDetailView(ServiceDetailView):
    model = PlanningAndDecor
    serializer_class = PlanningAndDecorSerializer

class PhotographyListView(ServiceListView):
    model = Photography
    serializer_class = PhotographySerializer

class PhotographyDetailView(ServiceDetailView):
    model = Photography
    serializer_class = PhotographySerializer

class MakeupListView(ServiceListView):
    model = Makeup
    serializer_class = MakeupSerializer

class MakeupDetailView(ServiceDetailView):
    model = Makeup
    serializer_class = MakeupSerializer

class BridalWearListView(ServiceListView):
    model = BridalWear
    serializer_class = BridalWearSerializer

class BridalWearDetailView(ServiceDetailView):
    model = BridalWear
    serializer_class = BridalWearSerializer

class GroomWearListView(ServiceListView):
    model = GroomWear
    serializer_class = GroomWearSerializer

class GroomWearDetailView(ServiceDetailView):
    model = GroomWear
    serializer_class = GroomWearSerializer

class MehandiListView(ServiceListView):
    model = Mehandi
    serializer_class = MehandiSerializer

class MehandiDetailView(ServiceDetailView):
    model = Mehandi
    serializer_class = MehandiSerializer

class WeddingCakeListView(ServiceListView):
    model = WeddingCake
    serializer_class = WeddingCakeSerializer

class WeddingCakeDetailView(ServiceDetailView):
    model = WeddingCake
    serializer_class = WeddingCakeSerializer

class CarRentalListView(ServiceListView):
    model = CarRental
    serializer_class = CarRentalSerializer

class CarRentalDetailView(ServiceDetailView):
    model = CarRental
    serializer_class = CarRentalSerializer

class DJListView(ServiceListView):
    model = DJ
    serializer_class = DJSerializer

class DJDetailView(ServiceDetailView):
    model = DJ
    serializer_class = DJSerializer

class JewelryRentalListView(ServiceListView):
    model = JewelryRental
    serializer_class = JewelryRentalSerializer

class JewelryRentalDetailView(ServiceDetailView):
    model = JewelryRental
    serializer_class = JewelryRentalSerializer

class CateringListView(ServiceListView):
    model = Catering
    serializer_class = CateringSerializer

class CateringDetailView(ServiceDetailView):
    model = Catering
    serializer_class = CateringSerializer

class CartView(APIView):
    """View for managing user's shopping cart"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        quantity = request.data.get('quantity', 1)
        
        if not content_type or not object_id:
            return Response(
                {'error': 'content_type and object_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate content_type
        valid_types = [choice[0] for choice in CartItem.CONTENT_TYPE_CHOICES]
        if content_type not in valid_types:
            return Response(
                {'error': 'Invalid content_type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if object exists
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
        
        model_class = model_map.get(content_type)
        if not model_class:
            return Response(
                {'error': 'Invalid content_type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            obj = model_class.objects.get(pk=object_id)
        except model_class.DoesNotExist:
            return Response(
                {'error': 'Object not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        existing_item = cart.items.filter(
            content_type=content_type,
            object_id=object_id
        ).first()
        
        if existing_item:
            existing_item.quantity += int(quantity)
            existing_item.save()
        else:
            new_item = CartItem.objects.create(
                content_type=content_type,
                object_id=object_id,
                quantity=quantity
            )
            cart.items.add(new_item)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        
        if not content_type or not object_id:
            return Response(
                {'error': 'content_type and object_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart = get_object_or_404(Cart, user=request.user)
        item = cart.items.filter(
            content_type=content_type,
            object_id=object_id
        ).first()
        
        if item:
            cart.items.remove(item)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Item not found in cart'},
            status=status.HTTP_404_NOT_FOUND
        )

class CartItemView(APIView):
    """View for managing individual cart items"""
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, item_id):
        quantity = request.data.get('quantity')
        
        if not quantity:
            return Response(
                {'error': 'quantity is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            item = CartItem.objects.get(pk=item_id)
            cart = Cart.objects.get(user=request.user, items=item)
        except (CartItem.DoesNotExist, Cart.DoesNotExist):
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        item.quantity = quantity
        item.save()
        return Response(CartItemSerializer(item).data)
    
    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(pk=item_id)
            cart = Cart.objects.get(user=request.user, items=item)
            cart.items.remove(item)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (CartItem.DoesNotExist, Cart.DoesNotExist):
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class WishlistView(APIView):
    """View for managing user's wishlist"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    def post(self, request):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        
        if not content_type or not object_id:
            return Response(
                {'error': 'content_type and object_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_fields = [
            'venues', 'planning_decor', 'photography', 'makeup',
            'bridal_wear', 'groom_wear', 'mehandi', 'wedding_cake',
            'car_rentals', 'djs', 'jewelry_rentals', 'catering'
        ]
        
        if content_type not in valid_fields:
            return Response(
                {'error': 'Invalid content_type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        manager = getattr(wishlist, content_type)
        
        model_map = {
            'venues': Venue,
            'planning_decor': PlanningAndDecor,
            'photography': Photography,
            'makeup': Makeup,
            'bridal_wear': BridalWear,
            'groom_wear': GroomWear,
            'mehandi': Mehandi,
            'wedding_cake': WeddingCake,
            'car_rentals': CarRental,
            'djs': DJ,
            'jewelry_rentals': JewelryRental,
            'catering': Catering,
        }
        
        model_class = model_map.get(content_type)
        try:
            obj = model_class.objects.get(pk=object_id)
            if not manager.filter(pk=object_id).exists():
                manager.add(obj)
            return Response(WishlistSerializer(wishlist).data, status=status.HTTP_201_CREATED)
        except model_class.DoesNotExist:
            return Response(
                {'error': 'Object not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        
        if not content_type or not object_id:
            return Response(
                {'error': 'content_type and object_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_fields = [
            'venues', 'planning_decor', 'photography', 'makeup',
            'bridal_wear', 'groom_wear', 'mehandi', 'wedding_cake',
            'car_rentals', 'djs', 'jewelry_rentals', 'catering'
        ]
        
        if content_type not in valid_fields:
            return Response(
                {'error': 'Invalid content_type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        wishlist = get_object_or_404(Wishlist, user=request.user)
        manager = getattr(wishlist, content_type)
        
        try:
            obj = manager.get(pk=object_id)
            manager.remove(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {'error': 'Item not found in wishlist'},
                status=status.HTTP_404_NOT_FOUND
            )

from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

class GlobalSearchView(APIView):
    """Search across all vendor types with minimal query requirements"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # Extract parameters from request body
            params = request.data
            
            # Check if at least one search parameter is provided
            if not any([
                params.get('q'),
                params.get('location'),
                params.get('vendor_type'),
                params.get('category'),
                params.get('min_price'),
                params.get('max_price'),
                params.get('min_rating'),
                params.get('min_capacity'),
                params.get('max_capacity')
            ]):
                return Response({
                    'success': False,
                    'error': 'At least one search parameter is required',
                    'timestamp': timezone.now().isoformat()
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract and validate parameters
            search_params = {
                'search_term': params.get('q', '').strip(),
                'location': params.get('location', '').strip(),
                'vendor_type': params.get('vendor_type', '').strip(),
                'category': params.get('category', '').strip(),
                'min_price': self.safe_float(params.get('min_price')),
                'max_price': self.safe_float(params.get('max_price')),
                'min_rating': self.safe_float(params.get('min_rating')),
                'min_capacity': self.safe_int(params.get('min_capacity')),
                'max_capacity': self.safe_int(params.get('max_capacity')),
                'page': self.safe_int(params.get('page', 1)),
                'page_size': self.safe_int(params.get('page_size', 20)),
            }
            
            # Perform search
            results = self.perform_search(search_params)
            
            return Response({
                'success': True,
                'data': results,
                'filters': search_params,
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def safe_float(self, value):
        """Safely convert to float, return None if invalid"""
        try:
            return float(value) if value not in [None, ''] else None
        except (ValueError, TypeError):
            return None
    
    def safe_int(self, value):
        """Safely convert to int, return default if invalid"""
        try:
            return int(value) if value not in [None, ''] else None
        except (ValueError, TypeError):
            return None
    
    def perform_search(self, params):
        """Perform search with minimal query requirements"""
        results = {}
        
        vendor_models = {
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
        
        models_to_search = [params['vendor_type']] if params['vendor_type'] else vendor_models.keys()
        
        for model_key in models_to_search:
            if model_key in vendor_models:
                model_class, serializer_class = vendor_models[model_key]
                queryset = model_class.objects.all()
                
                # Apply search term (optional)
                if params['search_term']:
                    queryset = queryset.filter(
                        Q(name__icontains=params['search_term']) |
                        Q(location__icontains=params['search_term']) |
                        Q(category__icontains=params['search_term']) |
                        Q(description__icontains=params['search_term'])
                    )
                
                # Apply location filter (optional)
                if params['location']:
                    queryset = queryset.filter(location__icontains=params['location'])
                
                # Apply category filter (optional)
                if params['category']:
                    queryset = queryset.filter(category=params['category'])
                
                # Apply price filters (optional)
                if params['min_price'] is not None:
                    if hasattr(model_class, 'price'):
                        queryset = queryset.filter(price__gte=params['min_price'])
                    elif hasattr(model_class, 'price_range_min'):
                        queryset = queryset.filter(price_range_min__gte=params['min_price'])
                    elif hasattr(model_class, 'price_per_plate'):
                        queryset = queryset.filter(price_per_plate__gte=params['min_price'])
                
                if params['max_price'] is not None:
                    if hasattr(model_class, 'price'):
                        queryset = queryset.filter(price__lte=params['max_price'])
                    elif hasattr(model_class, 'price_range_max'):
                        queryset = queryset.filter(price_range_max__lte=params['max_price'])
                    elif hasattr(model_class, 'price_per_plate'):
                        queryset = queryset.filter(price_per_plate__lte=params['max_price'])
                
                # Apply rating filter (optional)
                if params['min_rating'] is not None:
                    queryset = queryset.filter(rating__gte=params['min_rating'])
                
                # Apply capacity filters (optional - for venues and car rentals)
                if params['min_capacity'] is not None and hasattr(model_class, 'capacity'):
                    queryset = queryset.filter(capacity__gte=params['min_capacity'])
                
                if params['max_capacity'] is not None and hasattr(model_class, 'capacity'):
                    queryset = queryset.filter(capacity__lte=params['max_capacity'])
                
                # Apply pagination
                paginator = Paginator(queryset, params['page_size'])
                try:
                    page_obj = paginator.page(params['page'])
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                
                results[model_key] = {
                    'results': serializer_class(page_obj, many=True).data,
                    'pagination': {
                        'current_page': params['page'],
                        'total_pages': paginator.num_pages,
                        'total_results': paginator.count,
                        'page_size': params['page_size']
                    }
                }
        
        return results