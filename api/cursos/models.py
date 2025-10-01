from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Curso(models.Model):
   """
    Modelo de Curso que representa um curso oferecido pela instituição.
    
    Attributes:
        id: Identificador único do curso (UUID).
        codigo: Código único do curso (string).
        nome: Nome do curso (string).
        descricao: Descrição detalhada do curso (string, opcional).
        ativo: Indica se o curso está ativo (booleano).
        carga_horaria_total: Carga horária total do curso (inteiro).

    #### Regras:
    - O código do curso deve ser único entre os cursos ativos.
    - A soma da carga horária das disciplinas associadas ao curso não pode exceder a carga horária total do curso.

    Methods:
    - clean: Valida se o código do curso é único entre os cursos ativos.
    - save: Sobrescreve o método save para garantir a validação antes de salvar.
    - can_add_disciplina_with_carga_horaria: Verifica se uma disciplina com uma dada carga horária
       pode ser adicionada ao curso sem exceder a carga horária total do curso.
    - total_disciplinas_ativas: Retorna o total de disciplinas ativas associadas ao curso.
    - soma_carga_horaria_disciplinas_ativas: Retorna a soma da carga horária das disciplinas ativas associadas ao curso.
    
    """
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    carga_horaria_total = models.IntegerField()

    class Meta:

        db_table = 'cursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def clean(self):
        super().clean()
        existing = Curso.objects.filter(
            codigo=self.codigo,
            ativo=True
        ).exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError(f'Já existe um curso ativo com o código {self.codigo}')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    @property
    def total_disciplinas_ativas(self):
        return self.disciplinas.filter(ativo=True).count()

    @property
    def soma_carga_horaria_disciplinas_ativas(self):
        return self.disciplinas.filter(ativo=True).aggregate(
            total=models.Sum('carga_horaria')
        )['total'] or 0

    def can_add_disciplina_with_carga_horaria(self, carga_horaria):
        soma_atual = self.soma_carga_horaria_disciplinas_ativas
        return (soma_atual + carga_horaria) <= self.carga_horaria_total