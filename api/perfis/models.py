from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid
from datetime import datetime


class Perfil(AbstractUser):
    """
    Modelo de Perfil que estende AbstractUser do Django.

    #### Tipo de Perfis:
    - Gerente
    - Professor

    Attributes:
        id (UUID): Chave primária.
        codigo (str): Código único no formato `MAT.AAAA.NNNN`.
        nome (str): Nome completo.
        tipo (str): "Gerente" ou "Professor".
        email (str): E-mail único usado como login.
        ativo (bool): Flag de atividade (soft on/off).
        USERNAME_FIELD (str): Campo de autenticação (`email`).
        REQUIRED_FIELDS (list[str]): Campos obrigatórios além do `email`

    ### Validação
    - Gera um código único no formato MAT.AAAA.NNNN.
    - Garante que o código seja único entre perfis ativos.
    """
    TIPO_CHOICES = [
        ('Gerente', 'Gerente'),
        ('Professor', 'Professor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    email = models.EmailField(unique=True)
    ativo = models.BooleanField(default=True)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'tipo']

    class Meta:
        db_table = 'perfis'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def save(self, *args, **kwargs):
        if not self.codigo:
            ano_atual = datetime.now().year
            ultimo_codigo = Perfil.objects.filter(
                codigo__startswith=f'MAT.{ano_atual}.'
            ).order_by('codigo').last()

            if ultimo_codigo:
                # Extrai apenas os números após o último ponto para ordenação numérica
                codigos_numericos = [
                    int(p.codigo.split('.')[-1])
                    for p in Perfil.objects.filter(codigo__startswith=f'MAT.{ano_atual}.')
                ]
                ultimo_numero = max(
                    codigos_numericos) if codigos_numericos else 0
                proximo_numero = ultimo_numero + 1
            else:
                proximo_numero = 1

            self.codigo = f'MAT.{ano_atual}.{proximo_numero}'

        existing = Perfil.objects.filter(
            codigo=self.codigo,
            ativo=True
        ).exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError(
                f'Já existe um perfil ativo com o código {self.codigo}')

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'
