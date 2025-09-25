from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Curso(models.Model):
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