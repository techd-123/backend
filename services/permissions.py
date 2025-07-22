from rest_framework.permissions import BasePermission

class IsStaffOrReadOnly(BasePermission):
    """
    Allows creation only by staff users, but allows read access to anyone.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff

class IsCreatorOrReadOnly(BasePermission):
    """
    Allows edit/delete only by the creator of the object, but allows read access to anyone.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.creator == request.user

class IsStaffOrCreatorOrReadOnly(IsStaffOrReadOnly, IsCreatorOrReadOnly):
    """
    Combines both permissions:
    - Staff can create and edit/delete any
    - Creators can edit/delete their own
    - Anyone can read
    """
    def has_permission(self, request, view):
        return IsStaffOrReadOnly.has_permission(self, request, view)
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return IsCreatorOrReadOnly.has_object_permission(self, request, view, obj)