from rest_framework import serializers
from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Perfil.

    Attributes:
        password (str): Campo write-only opcional para a senha do perfil.
        get_full_name (str): Campo read-only que retorna o nome completo do perfil.

    ### Campos
    - id
    - codigo
    - nome
    - get_full_name (read-only)
    - tipo
    - email
    - password (write-only, opcional)
    - ativo
    """
    password = serializers.CharField(write_only=True, required=False)
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = Perfil
        fields = [
            'id', 'codigo', 'nome', 'get_full_name', 'tipo', 'email', 'password', 'ativo'
        ]
        # Campos adicionais para controle de acesso e segurança
        extra_kwargs = {
            'password': {'write_only': True},
            'codigo': {'read_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        # Campos permitidos para criação
        allowed_fields = ['nome', 'tipo', 'email', 'ativo']
        create_data = {k: v for k, v in validated_data.items()
                       if k in allowed_fields}

        perfil = Perfil.objects.create(**create_data)
        perfil.set_password(password)
        return perfil

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Campos permitidos para atualização
        allowed_fields = ['nome', 'tipo', 'email', 'ativo']

        for attr, value in validated_data.items():
            if attr in allowed_fields:
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
    - nome
    - get_full_name (read-only)
    - tipo
    - email
    - ativo
    """
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = Perfil
        fields = ['id', 'codigo', 'nome',
                  'get_full_name', 'tipo', 'email', 'ativo']


class PerfilMeSerializer(serializers.ModelSerializer):
    """
    Serializer para o perfil do usuário autenticado.

    ### Campos
    - id
    - nome
    - get_full_name (read-only)
    - email
    - tipo
    - ativo
    """
    get_full_name = serializers.ReadOnlyField()

    class Meta:
        model = Perfil
        fields = ['id', 'nome', 'get_full_name', 'email', 'tipo', 'ativo']
