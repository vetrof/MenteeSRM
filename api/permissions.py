from rest_framework import permissions


class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешение для чтения (GET, HEAD, OPTIONS) всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение на изменение (PUT, DELETE) только суперпользователю
        return request.user and request.user.is_superuser