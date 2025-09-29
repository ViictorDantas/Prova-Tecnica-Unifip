from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Perfil
from .serializers import PerfilSerializer, PerfilListSerializer, PerfilMeSerializer
from .permissions import IsGerente, IsProfessorOuGerenteOuSomenteLeitura


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'tipo']
    search_fields = ['email',
                     'nome', 'codigo']  
    ordering_fields = ['email', 'tipo', 'ativo', 'nome', 'codigo']
    ordering = ['email'] 

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'inativar', 'ativar']:
            self.permission_classes = [IsGerente]
        else:
            self.permission_classes = [IsProfessorOuGerenteOuSomenteLeitura]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        perfil = request.user
        serializer = PerfilMeSerializer(perfil)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return PerfilListSerializer
        if self.action == 'me':
            return PerfilMeSerializer
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
