from django.contrib import admin
from .models import Disciplina


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'curso', 'carga_horaria', 'ativo')
    list_filter = ('ativo', 'curso')
    search_fields = ('codigo', 'nome', 'curso__nome', 'curso__codigo')
    ordering = ('codigo',)