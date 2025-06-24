from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Permission to only allow owners of a profile to edit or delete it.
    Read-only access is allowed for any request.
    """
    message = "Only the owner is allowed to change or delete."

    def has_object_permission(self, request, view, obj):
        """
        Check permissions for profile object:
        - SAFE_METHODS (GET, HEAD, OPTIONS) are always allowed.
        - Other methods require the profile owner.

        Args:
            request (Request): The current HTTP request.
            view (View): The view being accessed.
            obj (Profile): The profile instance.

        Returns:
            bool: True if permission is granted, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user