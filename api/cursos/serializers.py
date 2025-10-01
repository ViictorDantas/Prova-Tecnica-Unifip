from rest_framework import serializers
from .models import Curso


class CursoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Disciplina.

    Attributes:
        total_disciplinas_ativas (int): Número total de disciplinas ativas no curso.
        soma_carga_horaria_disciplinas_ativas (int): Soma da carga horária das disciplinas ativas no curso.

    ### Campos
    - id
    - codigo
    - nome
    - descricao
    - ativo
    - carga_horaria_total
    - total_disciplinas_ativas (read-only)
    - soma_carga_horaria_disciplinas_ativas (read-only)
    """
    total_disciplinas_ativas = serializers.ReadOnlyField()
    soma_carga_horaria_disciplinas_ativas = serializers.ReadOnlyField()

    class Meta:
        model = Curso
        fields = [
            'id', 'codigo', 'nome', 'descricao', 'ativo', 'carga_horaria_total',
            'total_disciplinas_ativas', 'soma_carga_horaria_disciplinas_ativas'
        ]


class CursoListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar cursos com campos básicos.
    Os campos são id, codigo, nome, descricao, ativo e carga_horaria_total.
    """
    class Meta:
        model = Curso
        fields = ['id', 'codigo', 'nome', 'descricao',
                  'ativo', 'carga_horaria_total']


class CursoResumoSerializer(serializers.ModelSerializer):
    """
    Serializer para resumir informações do curso.

    Returns:
       - total_disciplinas_ativas (int): Número total de disciplinas ativas no curso.
       - soma_carga_horaria_disciplinas_ativas (int): Soma da carga horária das disciplinas ativas no curso.
    """
    total_disciplinas_ativas = serializers.ReadOnlyField()
    soma_carga_horaria_disciplinas_ativas = serializers.ReadOnlyField()

    class Meta:
        model = Curso
        fields = ['total_disciplinas_ativas',
                  'soma_carga_horaria_disciplinas_ativas']
