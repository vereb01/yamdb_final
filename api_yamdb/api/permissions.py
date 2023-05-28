from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Получение данных доступно для всех пользователей,
    изменять могут только админ или суперюзера.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """
    Получение данных доступно для всех пользователей,
    изменять может только админ, модератор, автор.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    """Предостовляет доступ только админу."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_staff
            or request.user.is_superuser)
