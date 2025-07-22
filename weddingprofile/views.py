from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import WeddingProfile
from .serializers import WeddingProfileSerializer
from .permissions import IsOwnerOrPartnerReadOnly

class WeddingProfileListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = WeddingProfile.objects.filter(
            Q(owner=request.user) | Q(partner=request.user))
        serializer = WeddingProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WeddingProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeddingProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrPartnerReadOnly]

    def get_object(self, pk):
        profile = get_object_or_404(WeddingProfile, pk=pk)
        self.check_object_permissions(self.request, profile)
        return profile

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = WeddingProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = WeddingProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        profile = self.get_object(pk)
        serializer = WeddingProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TogglePartnerEditPermissionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        profile = get_object_or_404(WeddingProfile, pk=pk)
        
        if profile.owner != request.user:
            return Response(
                {"detail": "Only the owner can change edit permissions."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        profile.partner_can_edit = not profile.partner_can_edit
        profile.save()
        return Response(
            {"partner_can_edit": profile.partner_can_edit},
            status=status.HTTP_200_OK
        )

class RemovePartnerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        profile = get_object_or_404(WeddingProfile, pk=pk)
        
        if profile.owner != request.user:
            return Response(
                {"detail": "Only the owner can remove partners."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        profile.partner = None
        profile.partner_can_edit = False
        profile.save()
        return Response(
            {"detail": "Partner removed successfully."},
            status=status.HTTP_200_OK
        )