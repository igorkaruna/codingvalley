from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow object's owners to interact with it.
    """

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class EmailVerified(IsOwner):

    def has_permission(self, request, view):
        return request.user.email_verified
