from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import Order, OrderItem, VendorOrderNotification
from .serializers import *
from services.models import *

class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get orders - customers see their orders, vendors see orders for their services"""
        if request.user.is_staff:
            # Staff can see all orders
            orders = Order.objects.all()
        elif hasattr(request.user, 'created_services'):
            # Vendor - see orders for their services
            vendor_orders = Order.objects.filter(
                items__vendor_email=request.user.email
            ).distinct()
            orders = vendor_orders
        else:
            # Customer - see their own orders
            orders = Order.objects.filter(customer=request.user)
        
        serializer = OrderSerializer(orders.order_by('-created_at'), many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        order = get_object_or_404(Order, pk=pk)
        
        # Check permissions
        if not (order.customer == self.request.user or 
                self.request.user.is_staff or
                order.items.filter(vendor_email=self.request.user.email).exists()):
            raise permissions.PermissionDenied("You don't have permission to view this order")
        
        return order
    
    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            items_data = serializer.validated_data['items']
            event_date = serializer.validated_data.get('event_date')
            special_instructions = serializer.validated_data.get('special_instructions', '')
            
            # Model mapping for service types
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
            
            # Create order
            order = Order.objects.create(
                customer=request.user,
                customer_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                customer_email=request.user.email,
                customer_phone=request.user.phone_number or '',
                event_date=event_date,
                special_instructions=special_instructions,
                total_amount=0  # Will be calculated
            )
            
            total_amount = 0
            order_items = []
            
            for item_data in items_data:
                service_type = item_data['service_type']
                service_id = item_data['service_id']
                quantity = item_data['quantity']
                
                # Get service model and object
                model_class = model_map.get(service_type)
                if not model_class:
                    return Response(
                        {'error': f'Invalid service type: {service_type}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    service_obj = model_class.objects.get(pk=service_id)
                except model_class.DoesNotExist:
                    return Response(
                        {'error': f'{service_type} with ID {service_id} not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Determine price
                if hasattr(service_obj, 'price'):
                    unit_price = service_obj.price
                elif hasattr(service_obj, 'price_range_min'):
                    unit_price = service_obj.price_range_min
                elif hasattr(service_obj, 'price_per_plate'):
                    unit_price = service_obj.price_per_plate
                else:
                    unit_price = 0
                
                item_total = unit_price * quantity
                total_amount += item_total
                
                # Create order item
                order_item = OrderItem(
                    order=order,
                    service_type=service_type,
                    service_id=service_id,
                    service_name=service_obj.name,
                    service_price=unit_price,
                    vendor_name=service_obj.creator.get_full_name() if service_obj.creator else 'Unknown Vendor',
                    vendor_email=service_obj.creator.email if service_obj.creator else '',
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=item_total,
                    service_date=item_data.get('service_date'),
                    service_time=item_data.get('service_time'),
                    notes=item_data.get('notes', '')
                )
                order_items.append(order_item)
            
            # Save all order items
            OrderItem.objects.bulk_create(order_items)
            
            # Update order total
            order.total_amount = total_amount
            order.save()
            
            # Send notifications to vendors
            self.send_vendor_notifications(order)
            
            # Send confirmation to customer
            self.send_customer_confirmation(order)
            
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_vendor_notifications(self, order):
        """Send email notifications to vendors about the new order"""
        vendors = order.get_vendors()
        
        for vendor in vendors:
            # Create notification record
            notification, created = VendorOrderNotification.objects.get_or_create(
                order=order,
                vendor=vendor
            )
            
            # Send email
            vendor_items = order.items.filter(vendor_email=vendor.email)
            
            subject = f'New Order Received - #{order.order_number}'
            html_message = render_to_string('emails/vendor_order_notification.html', {
                'vendor': vendor,
                'order': order,
                'items': vendor_items,
                'site_url': settings.FRONTEND_URL or 'http://localhost:3000'
            })
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [vendor.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                notification.email_sent = True
                notification.email_sent_at = timezone.now()
                notification.save()
            except Exception as e:
                print(f"Failed to send email to vendor {vendor.email}: {str(e)}")
    
    def send_customer_confirmation(self, order):
        """Send order confirmation email to customer"""
        subject = f'Order Confirmation - #{order.order_number}'
        html_message = render_to_string('emails/customer_order_confirmation.html', {
            'order': order,
            'customer': order.customer,
            'site_url': settings.FRONTEND_URL or 'http://localhost:3000'
        })
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [order.customer_email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send confirmation email to customer: {str(e)}")

class VendorOrdersView(APIView):
    """View for vendors to see their orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get orders where vendor has services
        orders = Order.objects.filter(
            items__vendor_email=request.user.email
        ).distinct().order_by('-created_at')
        
        # Get notifications for these orders
        notifications = VendorOrderNotification.objects.filter(
            vendor=request.user,
            order__in=orders
        )
        
        orders_serializer = OrderSerializer(orders, many=True)
        notifications_serializer = VendorOrderNotificationSerializer(notifications, many=True)
        
        return Response({
            'orders': orders_serializer.data,
            'notifications': notifications_serializer.data,
            'total_orders': orders.count(),
            'pending_orders': orders.filter(order_status='pending').count(),
            'unviewed_notifications': notifications.filter(viewed=False).count()
        })

class UpdateOrderStatusView(APIView):
    """Allow vendors to update order status"""
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        # Check if user is a vendor for this order
        if not order.items.filter(vendor_email=request.user.email).exists() and not request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to update this order")
        
        new_status = request.data.get('order_status')
        if new_status not in dict(Order.ORDER_STATUS_CHOICES):
            return Response(
                {'error': 'Invalid order status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.order_status = new_status
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class MarkNotificationViewedView(APIView):
    """Mark vendor notifications as viewed"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, notification_id):
        notification = get_object_or_404(
            VendorOrderNotification, 
            id=notification_id, 
            vendor=request.user
        )
        
        if not notification.viewed:
            notification.viewed = True
            notification.viewed_at = timezone.now()
            notification.save()
        
        return Response({'message': 'Notification marked as viewed'})