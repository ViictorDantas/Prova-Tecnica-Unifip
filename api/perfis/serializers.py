from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Disciplina.

    Attributes:
        password (str): Campo write-only para a senha do perfil.
        get_full_name (str): Campo read-only que retorna o nome completo do perfil.

    ### Campos
    - id
    - codigo
    - get_full_name (read-only)
    - tipo
    - email
    - password (write-only)
    - ativo
    """
    password = serializers.CharField(write_only=True)
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = Perfil
        fields = [
            'id', 'codigo', 'get_full_name', 'tipo', 'email', 'password', 'ativo'
        ]
        # Campos adicionais para controle de acesso e segurança
        extra_kwargs = {
            'password': {'write_only': True},
            'codigo': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        perfil = Perfil.objects.create(**validated_data)
        perfil.set_password(password)
        return perfil

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class PerfilListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar perfis com campos básicos.

    ### Campos
    - id
    - codigo
    - get_full_name (read-only)
    - tipo
    - email
    - ativo
    """
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = Perfil
        fields = ['id', 'codigo', 'get_full_name', 'tipo', 'email', 'ativo']


class PerfilMeSerializer(serializers.ModelSerializer):
    """
    Serializer para o perfil do usuário autenticado.

    ### Campos
    - id
    - get_full_name (read-only)
    - email
    - tipo
    - ativo
    """
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = Perfil
        fields = ['id', 'get_full_name', 'email', 'tipo', 'ativo']
