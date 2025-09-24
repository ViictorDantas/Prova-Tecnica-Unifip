import os
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramal_unifip.settings')
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from colaboradores.models import CustomUser

def create_superuser_if_not_exists(
    nome_colaborador,
    sexo,
    email,
    password,
    necessidade_especial=None,
    estado_civil=None,
    telefone=None,
    whatsapp=None,
    nacionalidade=None,
    raca=None,
    instagram=None,
    linkedin=None,
    foto=None,):
    
    # Tenta obter o colaborador pelo email
    try:
        existing_colaborador = CustomUser.objects.get(email=email)

        return existing_colaborador

    # Se não existir, cria um novo colaborador e o usuário associado
    except ObjectDoesNotExist:
        user = CustomUser.objects.create_superuser(
            email=email,
            password=password,
            nome_colaborador=nome_colaborador,
            sexo=sexo,
            necessidade_especial=necessidade_especial,
            estado_civil=estado_civil,
            numero_tel=telefone,
            numero_whatsapp=whatsapp,
            nacionalidade=nacionalidade,
            raca=raca,
            instagram=instagram,
            linkedin=linkedin,
            photo=foto
        )
        user.save()

        return user

# Criando colaboradores
superuser = create_superuser_if_not_exists(
    nome_colaborador='admin',
    sexo='M',
    email='admin@admin.com',
    password='admin',
    necessidade_especial='M',
    estado_civil='S',
    telefone='123456789',
    whatsapp='987654321',
    nacionalidade='Brasileiro',
    raca='BR',
    instagram='adminI',
    linkedin='adminL',
    foto=None,
)

exit()