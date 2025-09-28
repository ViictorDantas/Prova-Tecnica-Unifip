from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Disciplina
from .serializers import DisciplinaSerializer, DisciplinaListSerializer
from perfis.permissions import IsGerente, IsProfessorOuGerenteOuSomenteLeitura


class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    permission_classes = [IsProfessorOuGerenteOuSomenteLeitura]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'curso']
    search_fields = ['nome', 'codigo']
    ordering_fields = ['codigo', 'nome', 'carga_horaria']
    ordering = ['codigo']

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
