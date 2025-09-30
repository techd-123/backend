# orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Order, OrderItem, VendorOrderNotification
from .serializers import OrderSerializer, CreateOrderSerializer, OrderItemSerializer, VendorOrderNotificationSerializer
from services.models import *
from django.utils import timezone

User = get_user_model()

class OrderListView(APIView):
    """List all orders for the authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class CreateOrderView(APIView):
    """Create a new order"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create the order
                order = Order.objects.create(
                    customer=request.user,
                    customer_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                    customer_email=request.user.email,
                    customer_phone=request.user.phone_number or '',
                    event_date=serializer.validated_data.get('event_date'),
                    special_instructions=serializer.validated_data.get('special_instructions', ''),
                    total_amount=0  # Will be calculated
                )
                
                total_amount = 0
                order_items = []
                
                # Create order items
                for item_data in serializer.validated_data['items']:
                    service_type = item_data['service_type']
                    service_id = item_data['service_id']
                    quantity = item_data.get('quantity', 1)
                    
                    # Get the service object
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
                    
                    model_class = model_map.get(service_type)
                    if not model_class:
                        continue
                    
                    try:
                        service_obj = model_class.objects.get(pk=service_id)
                        
                        # Calculate prices
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
                        
                    except model_class.DoesNotExist:
                        continue
                
                # Save all order items
                OrderItem.objects.bulk_create(order_items)
                
                # Update order total
                order.total_amount = total_amount
                order.save()
                
                # Send vendor notifications
                self.send_vendor_notifications(order)
                self.send_customer_confirmation(order)
                
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to create order: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_vendor_notifications(self, order):
        """Send email notifications to vendors"""
        from django.core.mail import send_mail
        from django.conf import settings
        from django.utils import timezone
        
        vendors = order.get_vendors()
        
        for vendor in vendors:
            notification, created = VendorOrderNotification.objects.get_or_create(
                order=order,
                vendor=vendor
            )
            
            vendor_items = order.items.filter(vendor_email=vendor.email)
            
            subject = f'New Order Received - #{order.order_number}'
            
            message = f"""
            New Order Received!
            
            Order Number: #{order.order_number}
            Customer: {order.customer_name}
            Email: {order.customer_email}
            Phone: {order.customer_phone}
            Event Date: {order.event_date}
            
            Services Ordered:
            """
            
            for item in vendor_items:
                message += f"\n- {item.service_name}: {item.quantity} x ₹{item.unit_price} = ₹{item.total_price}"
            
            message += f"\n\nTotal Amount: ₹{order.total_amount}"
            
            if order.special_instructions:
                message += f"\n\nSpecial Instructions: {order.special_instructions}"
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [vendor.email],
                    fail_silently=False,
                )
                notification.email_sent = True
                notification.email_sent_at = timezone.now()
                notification.save()
            except Exception as e:
                print(f"Failed to send email to vendor {vendor.email}: {str(e)}")
    
    def send_customer_confirmation(self, order):
        """Send order confirmation to customer"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f'Order Confirmation - #{order.order_number}'
        
        message = f"""
        Thank you for your order!
        
        Order Number: #{order.order_number}
        Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}
        Total Amount: ₹{order.total_amount}
        Status: {order.get_order_status_display()}
        
        Your vendors have been notified and will contact you shortly.
        
        Thank you for choosing our service!
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [order.customer_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send confirmation email to customer: {str(e)}")

class OrderDetailView(APIView):
    """Retrieve, update or delete an order instance"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, customer=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class UpdateOrderStatusView(APIView):
    """Update order status and payment status"""
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        # Check if user is customer or vendor associated with the order
        is_customer = order.customer == request.user
        is_vendor = order.items.filter(vendor_email=request.user.email).exists()
        
        if not (is_customer or is_vendor or request.user.is_staff):
            return Response(
                {'error': 'You do not have permission to update this order'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        order_status = request.data.get('order_status')
        payment_status = request.data.get('payment_status')
        
        updates = {}
        if order_status and order_status in dict(Order.ORDER_STATUS_CHOICES):
            updates['order_status'] = order_status
        
        if payment_status and payment_status in dict(Order.PAYMENT_STATUS_CHOICES):
            updates['payment_status'] = payment_status
        
        if not updates:
            return Response(
                {'error': 'No valid status updates provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update the order
        for field, value in updates.items():
            setattr(order, field, value)
        
        order.save()
        
        serializer = OrderSerializer(order)
        return Response({
            'message': 'Order status updated successfully',
            'order': serializer.data
        })

class VendorOrdersView(APIView):
    """Get all orders for a vendor"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get orders where vendor email matches current user's email
        orders = Order.objects.filter(
            items__vendor_email=request.user.email
        ).distinct().order_by('-created_at')
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class MarkNotificationViewedView(APIView):
    """Mark vendor notification as viewed"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, notification_id):
        notification = get_object_or_404(
            VendorOrderNotification, 
            pk=notification_id, 
            vendor=request.user
        )
        
        if not notification.viewed:
            notification.viewed = True
            notification.viewed_at = timezone.now()
            notification.save()
        
        serializer = VendorOrderNotificationSerializer(notification)
        return Response({
            'message': 'Notification marked as viewed',
            'notification': serializer.data
        })