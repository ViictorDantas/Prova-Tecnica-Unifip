# Catálogo de Cursos & Disciplinas

Este é um projeto de uma API REST para gerenciar Cursos e Disciplinas, construído com Django + DRF + PostgreSQL e empacotado com Docker/Docker Compose.

## Tecnologias Utilizadas

- **Backend**: Django 5.2.6 + Django REST Framework 3.14.0
- **Banco de Dados**: PostgreSQL 16
- **Autenticação**: JWT (djangorestframework-simplejwt)
- **Documentação**: Swagger/OpenAPI (drf-spectacular)
- **Containerização**: Docker + Docker Compose

## Pré-requisitos

- Docker
- Docker Compose

## Setup e Execução

### 1. Clone o repositório
```bash
git clone <https://github.com/ViictorDantas/Prova-Tecnica-Unifip/tree/Integra%C3%A7%C3%A3o>
cd Prova-Tecnica-Unifip-main
```

### 2. Configuração do ambiente
O arquivo `.env` já está configurado em `dotenv_files/.env` com as seguintes variáveis:

```env
SECRET_KEY="django-insecure-your-secret-key-change-in-production"
DEBUG="1"
ALLOWED_HOSTS="127.0.0.1, localhost"
DB_ENGINE="django.db.backends.postgresql"
POSTGRES_DB="catalogodb"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres123"
POSTGRES_HOST="psql"
POSTGRES_PORT="5432"
```

### 3. Construir e executar os containers
```bash
# Iniciar Docker Desktop (se estiver no macOS/Windows)
# ou certificar que o daemon Docker está rodando

# Construir e executar os containers
docker compose up --build

# Para executar em segundo plano (detached mode)
docker compose up --build -d
```

### 4. Executar migrações e criar superusuário
```bash
# Executar migrações
docker compose exec djangoapp python manage.py migrate

# Criar superusuário
docker compose exec djangoapp python manage.py createsuperuser
```

### 5. Acessar a aplicação

- **API**: http://localhost:8000/
- **Swagger/OpenAPI**: http://localhost:8000/swagger/
- **Admin Django**: http://localhost:8000/admin/

## Estrutura do Projeto

```
├── djangoapp/              # Aplicação Django
│   ├── api/               # Configurações principais
│   ├── perfis/            # App para gerenciar perfis de usuários
│   ├── cursos/            # App para gerenciar cursos
│   ├── disciplinas/       # App para gerenciar disciplinas
│   └── manage.py
├── scripts/               # Scripts de inicialização
├── dotenv_files/          # Arquivos de ambiente
├── docker-compose.yml     # Configuração Docker Compose
├── Dockerfile             # Configuração Docker
└── README.md
```

## API Endpoints

### Autenticação
- `POST /auth/token/` - Obter token JWT
- `POST /auth/token/refresh/` - Renovar token JWT

### Documentação
- `GET /swagger/` - Interface Swagger/OpenAPI

### Perfis (TODO)
- `GET /perfis/` - Listar perfis
- `POST /perfis/` - Criar perfil
- `GET /perfis/{id}/` - Detalhar perfil
- `PUT/PATCH /perfis/{id}/` - Atualizar perfil

### Cursos (TODO)
- `GET /cursos/` - Listar cursos
- `POST /cursos/` - Criar curso
- `GET /cursos/{id}/` - Detalhar curso
- `PUT/PATCH /cursos/{id}/` - Atualizar curso

### Disciplinas (TODO)
- `GET /disciplinas/` - Listar disciplinas
- `POST /disciplinas/` - Criar disciplina
- `GET /disciplinas/{id}/` - Detalhar disciplina
- `PUT/PATCH /disciplinas/{id}/` - Atualizar disciplina

## Comandos Úteis

```bash
# Ver logs dos containers
docker compose logs

# Parar os containers
docker compose down

# Entrar no container da aplicação
docker compose exec djangoapp bash

# Executar comandos Django
docker compose exec djangoapp python manage.py <comando>

# Rebuild completo (limpar cache)
docker compose down
docker compose build --no-cache
docker compose up
```

## API Endpoints Implementados

### Autenticação
- `POST /auth/token/` - Obter token JWT
- `POST /auth/token/refresh/` - Renovar token JWT

### Documentação
- `GET /swagger/` - Interface Swagger/OpenAPI
- `GET /schema/` - Schema OpenAPI

### Perfis
- `GET /perfis/` - Listar perfis (com filtros: ativo, codigo, tipo)
- `POST /perfis/` - Criar perfil
- `GET /perfis/{id}/` - Detalhar perfil
- `PUT/PATCH /perfis/{id}/` - Atualizar perfil
- `PATCH /perfis/{id}/inativar/` - Inativar perfil
- `PATCH /perfis/{id}/ativar/` - Ativar perfil
- `DELETE /perfis/{id}/` - Excluir perfil

### Cursos
- `GET /cursos/` - Listar cursos (com filtros: ativo, codigo)
- `POST /cursos/` - Criar curso
- `GET /cursos/{id}/` - Detalhar curso
- `PUT/PATCH /cursos/{id}/` - Atualizar curso
- `PATCH /cursos/{id}/inativar/` - Inativar curso
- `PATCH /cursos/{id}/ativar/` - Ativar curso
- `GET /cursos/{id}/resumo/` - Resumo do curso (total disciplinas e carga horária)
- `DELETE /cursos/{id}/` - Excluir curso

### Disciplinas
- `GET /disciplinas/` - Listar disciplinas (com filtros: curso, ativo)
- `POST /disciplinas/` - Criar disciplina
- `GET /disciplinas/{id}/` - Detalhar disciplina
- `PUT/PATCH /disciplinas/{id}/` - Atualizar disciplina
- `PATCH /disciplinas/{id}/inativar/` - Inativar disciplina
- `PATCH /disciplinas/{id}/ativar/` - Ativar disciplina
- `DELETE /disciplinas/{id}/` - Excluir disciplina

## Regras de Negócio Implementadas

Códigos únicos para perfis, cursos e disciplinas ativos
Geração automática de códigos para perfis (MAT.{ano}.{sequencial})
Validação de carga horária total dos cursos
Impossibilidade de adicionar disciplinas a cursos inativos
Soma das cargas horárias das disciplinas não pode exceder a carga total do curso
Autenticação JWT obrigatória
Permissões: apenas usuários Gerente podem fazer CRUD completo

## Status do Desenvolvimento

Configuração inicial do projeto
Configuração Docker/Docker Compose
Configuração Django + DRF
Configuração JWT e Swagger
Modelos implementados com validações
APIs REST completas
Validações de negócio
Sistema de permissões
Dados iniciais automáticos
Interface Admin
Frontend Django (implementado - páginas de login, listagem e detalhes de cursos, listagem de perfis)

## Credenciais de Acesso (Criadas automaticamente)

- **Gerente**: admin@example.com / admin123
- **Professor**: professor@example.com / prof123
