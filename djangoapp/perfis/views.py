from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Perfil
from .serializers import PerfilSerializer, PerfilListSerializer
from .permissions import IsGerente


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    permission_classes = [IsGerente]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'codigo', 'tipo']
    search_fields = ['nome', 'email', 'codigo']
    ordering_fields = ['codigo', 'nome', 'email']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.action == 'list':
            return PerfilListSerializer
        return PerfilSerializer

    @action(detail=True, methods=['patch'])
    def inativar(self, request, pk=None):
        perfil = self.get_object()
        perfil.ativo = False
        perfil.save()
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        perfil = self.get_object()
        perfil.ativo = True
        perfil.save()
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)