from rest_framework import serializers
from .models import Disciplina
from cursos.serializers import CursoListSerializer


class DisciplinaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Disciplina.

    Attributes:
        curso_detalhes (CursoListSerializer): Detalhes *read-only* do curso associado (`source='curso'`).

    ### Campos
    - id
    - codigo
    - nome
    - carga_horaria
    - curso (ID do curso)
    - curso_detalhes (detalhes do curso, somente leitura)
    - ativo
    """
    curso_detalhes = CursoListSerializer(source='curso', read_only=True)

    class Meta:
        model = Disciplina
        fields = [
            'id', 'codigo', 'nome', 'carga_horaria', 'curso',
            'curso_detalhes', 'ativo'
        ]


class DisciplinaListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar disciplinas com campos básicos e informações do curso.
    
    ### Campos:
    - id
    - codigo
    - nome
    - carga_horaria
    - curso (ID do curso)
    - curso_nome (Nome do curso)
    - curso_codigo (Código do curso)
    - ativo

    """
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    curso_codigo = serializers.CharField(source='curso.codigo', read_only=True)

    class Meta:
        model = Disciplina
        fields = [
            'id', 'codigo', 'nome', 'carga_horaria',
            'curso', 'curso_nome', 'curso_codigo', 'ativo'
        ]