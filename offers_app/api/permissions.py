from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBusinessUser(BasePermission):
    """
    Permission to allow only users with a business profile to create offers.
    """
    message = "Only users with business-profiles are allowed to create an offer."

    def has_permission(self, request, view):
        """
        Return True for safe methods or if the user is authenticated,
        has a profile, and profile.type == 'business' for POST requests.
        """
        if request.method == 'POST':
            return (
                request.user.is_authenticated and
                hasattr(request.user, 'profile') and
                request.user.profile.type == 'business'
            )
        return True

class IsOwnerOrReadOnly(BasePermission):
    """
    Permission to allow only the owner of an object to modify it.
    Safe methods are allowed for any request.
    """
    message = "Only the owner is allowed to change or delete."

    def has_object_permission(self, request, view, obj):
        """
        Return True for safe methods, else check if the requesting
        user is the owner of the object.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user