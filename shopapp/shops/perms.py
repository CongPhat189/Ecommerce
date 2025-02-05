from rest_framework import permissions



class OwnerAuthenticated(permissions.IsAuthenticated):
    message = 'You are not the owner of this comment'

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request,view) and request.user == obj.user