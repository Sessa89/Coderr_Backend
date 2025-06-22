from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBusinessUser(BasePermission):
    message = "Only users with business-profiles are allowed to create an offer."

    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user.is_authenticated and
                hasattr(request.user, 'profile') and
                request.user.profile.type == 'business'
            )
        return True

class IsOwnerOrReadOnly(BasePermission):
    message = "Only the owner is allowed to change or delete."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user