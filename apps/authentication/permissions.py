from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    """
    Custom permission class to allow only admin users.
    """

    def has_permission(self, request, view):
        if not request.user or request.user.role != "admin":
            raise PermissionDenied("You do not have permission to perform this action.")
        return True


class IsAdminOrCustomer(BasePermission):
    """
    Custom permission class to allow access to both admin and customer users.
    """

    def has_permission(self, request, view):
        if not request.user or request.user.role not in ["admin", "customer"]:
            raise PermissionDenied("You do not have permission to perform this action.")
        return True