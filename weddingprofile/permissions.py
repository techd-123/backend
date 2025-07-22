from rest_framework import permissions

class IsOwnerOrPartnerReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Owner has full access
    - Partner has read-only access unless partner_can_edit is True
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to partner
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.owner or request.user == obj.partner
        
        # Write permissions only for owner or partner if allowed
        if request.user == obj.owner:
            return True
        if request.user == obj.partner and obj.partner_can_edit:
            return True
        return False