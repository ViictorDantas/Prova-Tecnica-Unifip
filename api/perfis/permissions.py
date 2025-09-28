from rest_framework import permissions


class IsGerenteOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated and
            hasattr(request.user, 'tipo') and
            request.user.tipo == 'Gerente'
        )


class IsGerente(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'tipo') and
            request.user.tipo == 'Gerente'
        )


class IsProfessorOuGerenteOuSomenteLeitura(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user.is_authenticated and
                hasattr(request.user, 'tipo') and
                (request.user.tipo == 'Gerente' or request.user.tipo == 'Professor')
            )
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'tipo') and
            request.user.tipo == 'Gerente'
        )
