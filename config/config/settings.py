from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-key")
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', 'accounts', 'products', 'cart', 'orders','shipping',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.SimulationSecurityMiddleware',  # our per-session flags
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.simulation_mode',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default simulation mode if session has none.
SIMULATION_MODE = os.getenv('SIMULATION_MODE', 'secure')  # 'secure' or 'vulnerable'

# Security defaults for secure mode (middleware will toggle per-session flags)
SESSION_COOKIE_SECURE = False  # dev only
CSRF_COOKIE_SECURE = False     # dev only
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

AUTH_USER_MODEL = 'accounts.User'

VULNERABLE_LABS = {
    'csrf_disabled': False,
    'raw_sql_injection': True,
    'weak_password_hash': True
}


STRIPE_PUBLIC_KEY = "pk_test_51RwKMhJQHrTkAmKCC8L9UubCi6zH4DNrlg5suSmfEHFbfphLk1qirtarAct8SGrney8JdV0AaV8J73RXfcu8vIQc00DqkG4Uiq"
STRIPE_SECRET_KEY = "sk_test_51RwKMhJQHrTkAmKCB3pqysbatgXmnjLhSnnVE5CfKIvViLVvZAEfFHYBUSSdwTZaGGnRFhgEenVOVRQtqIstnwzU007evgPepL"
STRIPE_WEBHOOK_SECRET = "whsec_..."
