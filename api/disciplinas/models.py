from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Disciplina(models.Model):
    """
    Modelo para representar uma disciplina associada a um curso.
    Campos:
       - id (UUID): Identificador único da disciplina.
       - codigo (str): Código único da disciplina.
       - nome (str): Nome da disciplina.
       - carga_horaria (int): Carga horária da disciplina.
       - curso (ForeignKey): Referência ao curso ao qual a disciplina pertence.
       - ativo (bool): Indica se a disciplina está ativa ou inativa.

    Regras de Validação:
       - O código da disciplina deve ser único entre as disciplinas ativas.
       - Não é permitido adicionar uma disciplina a um curso inativado.
       - A soma da carga horária das disciplinas ativas de um curso não pode exceder
         a carga horária total do curso.
        
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    carga_horaria = models.IntegerField()
    curso = models.ForeignKey(
        'cursos.Curso',
        on_delete=models.CASCADE,
        related_name='disciplinas'
    )
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'disciplinas'
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def clean(self):
        """
        Validações a serem realizadas antes de salvar a disciplina.
        """
        super().clean()

        existing = Disciplina.objects.filter(
            codigo=self.codigo,
            ativo=True
        ).exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError(f'Já existe uma disciplina ativa com o código {self.codigo}')

        if self.curso and not self.curso.ativo:
            raise ValidationError('Não é possível adicionar disciplina a um curso inativado')

        if self.curso:
            outras_disciplinas_ativas = self.curso.disciplinas.filter(
                ativo=True
            ).exclude(pk=self.pk)

            soma_outras = sum(d.carga_horaria for d in outras_disciplinas_ativas)

            if (soma_outras + self.carga_horaria) > self.curso.carga_horaria_total:
                raise ValidationError(
                    f'A soma das cargas horárias das disciplinas ({soma_outras + self.carga_horaria}) '
                    f'não pode ultrapassar a carga horária total do curso ({self.curso.carga_horaria_total})'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'