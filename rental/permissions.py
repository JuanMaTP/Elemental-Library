from rest_framework import permissions


class IsRenterOrAdmin(permissions.BasePermission):
    """
    Only the person who borrowed the book unit, or a staff user, can act on a rental.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.person.user_id == request.user.id
