from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='index'),  # Nova home page
    path('cursos/', views.cursos_list_view,
         name='cursos_list'),  # Lista de cursos
    path('perfis/', views.perfis_list_view,
         name='perfis_list'),  # Lista de perfis
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cursos/<str:pk>/', views.curso_detail_view, name='curso_detail'),
]
