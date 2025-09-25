from django.contrib import admin
from .models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'carga_horaria_total', 'ativo', 'total_disciplinas_ativas')
    list_filter = ('ativo',)
    search_fields = ('codigo', 'nome', 'descricao')
    ordering = ('codigo',)

    def total_disciplinas_ativas(self, obj):
        return obj.total_disciplinas_ativas
    total_disciplinas_ativas.short_description = 'Disciplinas Ativas'