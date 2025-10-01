from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Curso
from .serializers import CursoSerializer, CursoListSerializer, CursoResumoSerializer
from perfis.permissions import IsGerente, IsProfessorOuGerenteOuSomenteLeitura


class CursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Curso, permitindo operações CRUD e ações customizadas.
    Como inativar, ativar e obter um resumo do curso.

    Returns:
        Response: Resposta HTTP com os dados do curso ou status da operação.

    **Regras**
    - Gerentes: criar, ler, atualizar, deletar, inativar e ativar cursos.
    - Professores: apenas ler cursos.
    """
    # Consultar todos os cursos
    queryset = Curso.objects.all()
    # Permitir filtragem, busca e ordenação
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    # Definir campos de filtragem
    filterset_fields = ['ativo', 'codigo']
    # Definir campos de busca
    search_fields = ['nome', 'codigo', 'descricao']
    # Definir campos de ordenação
    ordering_fields = ['codigo', 'nome', 'carga_horaria_total']
    # Definir ordenação padrão
    ordering = ['codigo']

    def get_permissions(self):
        """
        Define as permissões com base na ação.
        - Gerentes: criar, ler, atualizar, deletar, inativar e ativar cursos.
        - Professores: podem apenas ler cursos.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'inativar', 'ativar']:
            self.permission_classes = [IsGerente]
        else:
            self.permission_classes = [IsProfessorOuGerenteOuSomenteLeitura]
        return super().get_permissions()

    def get_serializer_class(self):
        """
        Retorna o serializer apropriado com base na ação.
        
        Sendo `CursoListSerializer` para listagem completa e `CursoSerializer` para com campos básicos.
        """
        if self.action == 'list':
            return CursoListSerializer
        return CursoSerializer

    @action(detail=True, methods=['patch'])
    def inativar(self, request, pk=None):
        """
        Inativa um curso.
        """
        curso = self.get_object()
        curso.ativo = False
        curso.save()
        serializer = self.get_serializer(curso)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        """
        Ativa um curso.
        """
        curso = self.get_object()
        curso.ativo = True
        curso.save()
        serializer = self.get_serializer(curso)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def resumo(self, request, pk=None):
        """
        Returns: um resumo de um curso.
        """
        curso = self.get_object()
        serializer = CursoResumoSerializer(curso)
        return Response(serializer.data)
