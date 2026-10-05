from rest_framework import permissions


class IsSelfOrReadOnly(permissions.BasePermission):
    """
    Anyone can read a profile; only the user themselves can change or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
