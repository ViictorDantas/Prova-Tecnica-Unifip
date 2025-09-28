from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisciplinaViewSet

router = DefaultRouter()
router.register(r'', DisciplinaViewSet, basename='disciplina')

urlpatterns = [
    path('', include(router.urls)),
]