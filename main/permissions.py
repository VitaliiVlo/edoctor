from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    The request from admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            (request.user and request.user.is_staff)
        )


class IsDoctor(BasePermission):
    """
    The request from doctor, nurse or admin.
    """

    def has_permission(self, request, view):
        return (
            request.user and request.user.can_change_visit()
        )
