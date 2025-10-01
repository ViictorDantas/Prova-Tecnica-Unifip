from rest_framework import permissions


class IsGerenteOrReadOnly(permissions.BasePermission):
    """
    Permite acesso somente a gerentes para métodos não seguros.
    Métodos seguros (GET, HEAD, OPTIONS) são permitidos para qualquer usuário autenticado. 

    ### Regras
    - Métodos seguros: Permitido para qualquer usuário autenticado.
    - Métodos não seguros: Permitido apenas para usuários com tipo 'Gerente'.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated and
            hasattr(request.user, 'tipo') and
            request.user.tipo == 'Gerente'
        )


class IsGerente(permissions.BasePermission):
    """
    Permite acesso somente a gerentes.
    
    ### Regras
    - Apenas usuários autenticados com tipo 'Gerente' têm permissão para fazer um CRUD completo.
    
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'tipo') and
            request.user.tipo == 'Gerente'
        )


class IsProfessorOuGerenteOuSomenteLeitura(permissions.BasePermission):
    """
    Permite acesso a gerentes e professores para métodos não seguros.

    ### Regras
    - Métodos seguros (GET, HEAD, OPTIONS): Permitido para usuários autenticados com tipo 'Gerente' ou 'Professor'.
    - Métodos não seguros (POST, PUT, PATCH, DELETE): Permitido apenas para usuários com tipo 'Gerente'.
    """
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
