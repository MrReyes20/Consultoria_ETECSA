from rest_framework import permissions

class IsConsultantOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado que solo permite acceso a consultores y administradores.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type in ['consultant', 'admin'] or 
            request.user.is_superuser
        )

class IsOwnerOrConsultant(permissions.BasePermission):
    """
    Permiso que permite a los usuarios ver/editar solo sus propios recursos,
    y a los consultores/admins ver todos.
    """
    def has_object_permission(self, request, view, obj):
        # Verificar si el objeto tiene un atributo de usuario
        if hasattr(obj, 'user'):
            owner = obj.user
        elif hasattr(obj, 'client'):
            owner = obj.client
        else:
            return False

        # Permitir acceso si el usuario es el propietario
        if owner == request.user:
            return True

        # Permitir acceso si el usuario es consultor o admin
        return request.user.user_type in ['consultant', 'admin'] or request.user.is_superuser

class IsAdminOnly(permissions.BasePermission):
    """
    Permiso que solo permite acceso a administradores.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type == 'admin' or 
            request.user.is_superuser
        )
