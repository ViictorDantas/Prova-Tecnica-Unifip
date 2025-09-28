from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Curso
from .serializers import CursoSerializer, CursoListSerializer, CursoResumoSerializer
from perfis.permissions import IsGerente, IsProfessorOuGerenteOuSomenteLeitura


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'codigo']
    search_fields = ['nome', 'codigo', 'descricao']
    ordering_fields = ['codigo', 'nome', 'carga_horaria_total']
    ordering = ['codigo']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'inativar', 'ativar']:
            self.permission_classes = [IsGerente]
        else:
            self.permission_classes = [IsProfessorOuGerenteOuSomenteLeitura]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return CursoListSerializer
        return CursoSerializer

    @action(detail=True, methods=['patch'])
    def inativar(self, request, pk=None):
        curso = self.get_object()
        curso.ativo = False
        curso.save()
        serializer = self.get_serializer(curso)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        curso = self.get_object()
        curso.ativo = True
        curso.save()
        serializer = self.get_serializer(curso)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def resumo(self, request, pk=None):
        curso = self.get_object()
        serializer = CursoResumoSerializer(curso)
        return Response(serializer.data)
