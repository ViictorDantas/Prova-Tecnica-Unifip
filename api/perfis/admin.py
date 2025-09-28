from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(UserAdmin):
    list_display = ('codigo', 'nome', 'email', 'tipo', 'ativo', 'date_joined')
    list_filter = ('tipo', 'ativo', 'date_joined')
    search_fields = ('codigo', 'nome', 'email')
    ordering = ('codigo',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'tipo')}),
        ('Permissões', {
            'fields': ('ativo', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'tipo', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('codigo', 'date_joined', 'last_login')