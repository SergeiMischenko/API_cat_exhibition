from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Кастомный permission"""

    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение разрешено для любого запроса, поэтому мы всегда будем
        # разрешать запросы GET, HEAD или OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Права на запись разрешены только автору сообщения или администратору
        return obj.owner == request.user or request.user.is_staff
