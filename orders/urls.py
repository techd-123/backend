from django.urls import path
from .views import *

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('vendor/orders/', VendorOrdersView.as_view(), name='vendor-orders'),
    path('vendor/notifications/<int:notification_id>/view/', MarkNotificationViewedView.as_view(), name='mark-notification-viewed'),
]