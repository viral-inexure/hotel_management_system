from rest_framework import permissions


class IsHeadOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.username == request.user


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action in permissions.SAFE_METHODS or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details,
        # allows staff to view all records.
        return obj == request.user or request.user.is_staff
