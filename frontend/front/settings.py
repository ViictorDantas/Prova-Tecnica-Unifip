# front/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / 'front.env')

SECRET_KEY = os.getenv('FRONTEND_SECRET_KEY', 'change-me')
DEBUG = bool(int(os.getenv('DEBUG', '1')))
ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    'ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'front.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'pages' / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'front.wsgi.application'

# Front não precisa de Postgres — usa SQLite só para sessões/admin
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': BASE_DIR / 'db.sqlite3'}}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

CSRF_TRUSTED_ORIGINS = ['http://localhost:8001', 'http://127.0.0.1:8001']

# URLs reais da API
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
INTERNAL_API_BASE_URL = os.getenv('INTERNAL_API_BASE_URL', API_BASE_URL)
API_TOKEN_URL = os.getenv(
    'API_TOKEN_URL', f'{INTERNAL_API_BASE_URL}/auth/token/')
API_REFRESH_URL = os.getenv(
    'API_REFRESH_URL', f'{INTERNAL_API_BASE_URL}/auth/token/refresh/')
