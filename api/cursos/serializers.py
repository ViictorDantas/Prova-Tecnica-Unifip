from rest_framework import serializers
from .models import Curso


class CursoSerializer(serializers.ModelSerializer):
    total_disciplinas_ativas = serializers.ReadOnlyField()
    soma_carga_horaria_disciplinas_ativas = serializers.ReadOnlyField()

    class Meta:
        model = Curso
        fields = [
            'id', 'codigo', 'nome', 'descricao', 'ativo', 'carga_horaria_total',
            'total_disciplinas_ativas', 'soma_carga_horaria_disciplinas_ativas'
        ]


class CursoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Curso
        fields = ['id', 'codigo', 'nome', 'descricao',
                  'ativo', 'carga_horaria_total']


class CursoResumoSerializer(serializers.ModelSerializer):
    total_disciplinas_ativas = serializers.ReadOnlyField()
    soma_carga_horaria_disciplinas_ativas = serializers.ReadOnlyField()

    class Meta:
        model = Curso
        fields = ['total_disciplinas_ativas',
                  'soma_carga_horaria_disciplinas_ativas']
