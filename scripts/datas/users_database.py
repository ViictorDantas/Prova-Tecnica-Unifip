import os
import django
from django.utils import timezone

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramal_unifip.settings')
django.setup()

from colaboradores.models import Colaborador
from endereco.models import Endereco, Local
from sede.models import CampusForaDeSede, InformacoesTramitacaoEmec
from setor.models import Setor

def criar_setor(nome_setor, localidade):

    # Verifica se o endereço já existe
    endereco = Endereco.objects.filter(
        logradouro='Rua Exemplo',
        numero='123',
        complemento='Apto 1',
        bairro='Centro',
        codigo_municipio='12345',
        nome_municipio='Cidade Exemplo',
        uf='EX'
    ).first()

    if not endereco:
        endereco = Endereco.objects.create(
            logradouro='Rua Exemplo',
            numero='123',
            complemento='Apto 1',
            bairro='Centro',
            codigo_municipio='12345',
            nome_municipio='Cidade Exemplo',
            uf='EX'
        )
        print('\n\nEndereço criado com sucesso!')
    else:
        print('Endereço já existe.')

    # Verifica se o local já existe
    local = Local.objects.filter(
        nome=localidade,
        endereco=endereco,
        bloco='1',
        sala='1',
        andar='Térreo'
    ).first()

    if not local:
        local = Local.objects.create(
            nome=localidade,
            endereco=endereco,
            bloco='1',
            sala='1',
            andar='Térreo'
        )
        print('Local criado com sucesso!')
    else:
        print('Local já existe.')

    # Verifica se a instância de InformacoesTramitacaoEmec já existe
    informacoes_tramitacao_emec = InformacoesTramitacaoEmec.objects.filter(
        numero_processo=123456
    ).first()

    if not informacoes_tramitacao_emec:
        informacoes_tramitacao_emec = InformacoesTramitacaoEmec.objects.create(
            numero_processo=123456,
            tipo_processo='Tipo Exemplo',
            data_cadastro=timezone.now(),
            data_protocolo=timezone.now(),
            codigo_emec=12345
        )
        print('Informações de tramitação EMEC criadas com sucesso!')
    else:
        print('Informações de tramitação EMEC já existem.')

    # Verifica se o Setor já existe
    setor = Setor.objects.filter(
        local=local,
        nome_setor=nome_setor,
        campus_fora_de_sede=informacoes_tramitacao_emec
    ).first()

    if not setor:
        setor = Setor.objects.create(
            turno='M',
            horario_inicio='08:00',
            horario_fim='12:00',
            nome_setor=nome_setor,
            local=local,
            ramal='1234',
            campus_fora_de_sede=informacoes_tramitacao_emec
        )
        print('Setor criado com sucesso!')
    else:
        print('Setor já existe.')

def criar_colaborador(email, nome_colaborador, nome_setor, 
                      nome_cargo, matricula, nome_localidade):
    
    verificador = False

    # Verifica se o colaborador já existe
    colaborador = Colaborador.objects.filter(
        matricula=matricula,
        email=email,
        nome_colaborador=nome_colaborador,
        is_staff=False,
    ).first()

    if not colaborador:
        novo_colaborador = Colaborador.objects.create(
            matricula=matricula,
            email=email,
            nome_colaborador=nome_colaborador,
            is_staff=False,
            cargo_colaborador=nome_cargo,
            carga_horaria='40h'
        )
        novo_colaborador.set_password('senha123')
        novo_colaborador.save()
        print('Colaborador criado com sucesso!')
        verificador = True
    else:
        print('Colaborador já existe.')

    if verificador == True:
        colaborador = novo_colaborador
    
    # Verifica se o setor já existe
    setor = Setor.objects.filter(
        local=Local.objects.filter(nome=nome_localidade).first(), 
        nome_setor=nome_setor
    ).first()

    if colaborador:
        if not setor:
            print('Setor não existe!')
        else:
            setor.colaboradores.add(colaborador)
            print('Colaborador adicionado ao setor existente.')

# Chama a função para criar os setores
criar_setor('Coordenação',
            'Medicina')

criar_setor('Secretaria',
            'Medicina')

criar_setor('Coordenação',
            'Biomedicina')

# Chama a função para criar os colaboradores
criar_colaborador('joao@teste.com',
                  'João',
                  'Coordenação',
                  'Coordenador',
                  '1001',
                  'Medicina')

criar_colaborador('maria@teste.com',
                  'Maria',
                  'Secretaria',
                  'Secretária',
                  '1002',
                  'Medicina')

criar_colaborador('pedro@teste.com',
                  'Pedro',
                  'Coordenação',
                  'Coordenador',
                  '1003',
                  'Biomedicina')