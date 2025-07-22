from django.urls import path
from .views import *

urlpatterns = [
    path('profiles/', WeddingProfileListCreateAPIView.as_view(), name='wedding-profile-list-create'),
    path('profiles/<int:pk>/', WeddingProfileDetailAPIView.as_view(), name='wedding-profile-detail'),
    path('profiles/<int:pk>/toggle-edit-permission/', TogglePartnerEditPermissionAPIView.as_view(), name='toggle-edit-permission'),
    path('profiles/<int:pk>/remove-partner/', RemovePartnerAPIView.as_view(), name='remove-partner'),
]