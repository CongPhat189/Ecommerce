from rest_framework import permissions


class OwnerPerms(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, instance):
        return super().has_permission(request, view) and request.user == instance.user
