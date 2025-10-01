from django.contrib import admin
from .models import Disciplina


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Disciplina, exibindo informações relevantes na interface administrativa do Django.
    """
    list_display = ('codigo', 'nome', 'curso', 'carga_horaria', 'ativo')
    list_filter = ('ativo', 'curso')
    search_fields = ('codigo', 'nome', 'curso__nome', 'curso__codigo')
    ordering = ('codigo',)