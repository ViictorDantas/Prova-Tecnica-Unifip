from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Perfil
        fields = [
            'id', 'codigo', 'nome', 'tipo', 'email', 'password', 'ativo'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'codigo': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        perfil = Perfil.objects.create(**validated_data)
        perfil.set_password(password)
        perfil.save()
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

    class Meta:
        model = Perfil
        fields = ['id', 'codigo', 'nome', 'tipo', 'email', 'ativo']