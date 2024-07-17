from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminRequiredPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.user.is_authenticated:
            return request.method in SAFE_METHODS


class AuthorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        else:
            return request.method in SAFE_METHODS


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.user_role == 'manager' or request.user.is_staff:
            return True
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.is_staff:
            return True
        return request.method in SAFE_METHODS
