"""
Configurações do Django para este projeto.

Este arquivo contém as configurações principais (settings) usadas pelo
projeto em ambiente de desenvolvimento. Ele foi gerado inicialmente pelo
comando `django-admin startproject` e foi enriquecido com comentários em
português para facilitar a manutenção.

Notas rápidas:
- Mantenha `SECRET_KEY` fora do repositório (usamos dotenv para carregar).
- `DEBUG` está ativado aqui — não use em produção.
"""

from pathlib import Path
import os
import dotenv

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do arquivo .env
dotenv.load_dotenv()

# Configurações de desenvolvimento - não adequadas para produção
# Veja https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Chave secreta usada para criptografia (deve ser mantida em segredo em produção)
SECRET_KEY = os.getenv('SECRET_KEY')

# Ativa o modo de depuração (não recomendado em produção)
DEBUG = True

# Lista de hosts permitidos para acessar o projeto
ALLOWED_HOSTS = []

# Definição dos aplicativos instalados no projeto
INSTALLED_APPS = [
    'django.contrib.admin',  # Interface administrativa do Django
    'django.contrib.auth',  # Sistema de autenticação
    'django.contrib.contenttypes',  # Framework para tipos de conteúdo
    'django.contrib.sessions',  # Gerenciamento de sessões
    'django.contrib.messages',  # Sistema de mensagens
    'django.contrib.staticfiles',  # Gerenciamento de arquivos estáticos

    # Aplicativos personalizados
    'apps.core',  # Aplicativo principal
    'apps.servicos',  # Aplicativo de serviços
    'widget_tweaks',  # Biblioteca para customização de formulários
    'apps.gerenciamento',  # Aplicativo de gerenciamento
]

# Middleware - camadas intermediárias de processamento de requisições/respostas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Segurança
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gerenciamento de sessões
    'django.middleware.common.CommonMiddleware',  # Funcionalidades comuns
    'django.middleware.csrf.CsrfViewMiddleware',  # Proteção contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticação
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensagens
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Proteção contra clickjacking
]

# Arquivo principal de URLs do projeto
ROOT_URLCONF = 'config.urls'

# Configurações de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend de templates do Django
        'DIRS': [BASE_DIR / 'templates'],  # Diretório de templates
        'APP_DIRS': True,  # Habilita busca de templates nos aplicativos
        'OPTIONS': {
            'context_processors': [  # Processadores de contexto
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração do WSGI (interface entre o servidor web e o Django)
WSGI_APPLICATION = 'config.wsgi.application'

# Configuração do banco de dados (SQLite por padrão)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Backend do banco de dados
        'NAME': BASE_DIR / 'db.sqlite3',  # Caminho do arquivo do banco de dados
    }
}

# Validações de senha para autenticação
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configurações de internacionalização
LANGUAGE_CODE = 'pt-br'  # Idioma padrão (português do Brasil)
TIME_ZONE = 'America/Sao_Paulo'  # Fuso horário
USE_I18N = True  # Habilita tradução
USE_TZ = True  # Habilita suporte a fuso horário


# Tipo de chave primária padrão para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLs para redirecionamento após login/logout
LOGIN_REDIRECT_URL = 'home'  # Redireciona para a página inicial após login
LOGIN_URL = 'login'  # URL para a página de login
LOGOUT_REDIRECT_URL = '/'  # Redireciona para a página inicial após logout

# Configurações de envio de e-mails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Servidor SMTP (exemplo: Gmail)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('GMAIL_API_KEY')  # Endereço de e-mail usado para envio
EMAIL_HOST_PASSWORD = os.getenv('SENHA')  # Senha do e-mail (use senhas de app para maior segurança)
DEFAULT_FROM_EMAIL = os.getenv('GMAIL_API_KEY')  # Endereço de e-mail padrão para envio


# Backends de autenticação
AUTHENTICATION_BACKENDS = [
    'apps.core.backends.EmailOrUsernameModelBackend',  # Backend personalizado para login via e-mail ou nome de usuário
    # 'django.contrib.auth.backends.ModelBackend',  # Backend padrão do Django (substituído pelo personalizado)
]

STATIC_URL = '/static/'  # URL base para arquivos estáticos
STATICFILES_DIRS = [BASE_DIR / "static"]  # Diretório adicional para arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')