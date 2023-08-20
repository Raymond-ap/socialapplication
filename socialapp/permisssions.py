from rest_framework.permissions import BasePermission

class IsGroupCreator(BasePermission):
    message = "You are not the creator of this group."

    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is the creator of the group
        return obj.creator == request.user