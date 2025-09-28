from rest_framework import serializers
from .models import Disciplina
from cursos.serializers import CursoListSerializer


class DisciplinaSerializer(serializers.ModelSerializer):
    curso_detalhes = CursoListSerializer(source='curso', read_only=True)

    class Meta:
        model = Disciplina
        fields = [
            'id', 'codigo', 'nome', 'carga_horaria', 'curso',
            'curso_detalhes', 'ativo'
        ]


class DisciplinaListSerializer(serializers.ModelSerializer):
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    curso_codigo = serializers.CharField(source='curso.codigo', read_only=True)

    class Meta:
        model = Disciplina
        fields = [
            'id', 'codigo', 'nome', 'carga_horaria',
            'curso', 'curso_nome', 'curso_codigo', 'ativo'
        ]