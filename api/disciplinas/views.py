from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Disciplina
from cursos.models import Curso  # Importar o modelo Curso
from .serializers import DisciplinaSerializer, DisciplinaListSerializer
from perfis.permissions import IsProfessorOuGerenteOuSomenteLeitura, IsGerente


class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'curso']
    search_fields = ['nome', 'codigo']
    ordering_fields = ['codigo', 'nome', 'carga_horaria']
    ordering = ['codigo']

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy', 'inativar', 'ativar']:
            self.permission_classes = [IsGerente]
        else:
            self.permission_classes = [IsProfessorOuGerenteOuSomenteLeitura]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        curso_id = request.data.get('curso')
        try:
            curso = Curso.objects.get(id=curso_id)
        except Curso.DoesNotExist:
            return Response({'detail': 'Curso não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        if not curso.ativo:
            return Response({'detail': 'Não é possível adicionar disciplina a um curso inativado.'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == 'list':
            return DisciplinaListSerializer
        return DisciplinaSerializer

    @action(detail=True, methods=['patch'])
    def inativar(self, request, pk=None):
        disciplina = self.get_object()
        disciplina.ativo = False
        disciplina.save()
        serializer = self.get_serializer(disciplina)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        disciplina = self.get_object()
        disciplina.ativo = True
        disciplina.save()
        serializer = self.get_serializer(disciplina)
        return Response(serializer.data)
