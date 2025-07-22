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