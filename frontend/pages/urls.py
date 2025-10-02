from django.urls import path
from . import views

urlpatterns = [
    # Home - agora renderiza página 404
    path('', views.page_404_view, name='index'),  # Página 404 como padrão
    path('home/', views.home_view, name='home'),  # Home original movida para /home/
    
    # Cursos
    path('cursos/', views.cursos_list_view,
         name='cursos_list'),  # Lista de cursos
    path('cursos/add/', views.add_curso_view,
         name='add_curso'),  # Adicionar curso
    path('cursos/<str:pk>/edit/', views.edit_curso_view,
         name='edit_curso'),  # Editar curso
    path('cursos/<str:pk>/', views.curso_detail_view, name='curso_detail'),
    
    # Perfis
    path('perfis/', views.perfis_list_view,
         name='perfis_list'),  # Lista de perfis
    path('perfis/add/', views.add_perfil_view,
         name='add_perfil'),  # Adicionar perfil
    path('perfis/<str:pk>/edit/', views.edit_perfil_view,
         name='edit_perfil'),  # Editar perfil
    path('perfis/<str:pk>/toggle/', views.toggle_perfil_ativo_view,
         name='toggle_perfil'),  # Ativar/inativar perfil
    
    # Login e Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
