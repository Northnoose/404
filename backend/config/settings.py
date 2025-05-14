import os
from django.utils.translation import gettext_lazy as _


# Definer BASE_DIR ved hjelp av os.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'api.urls'  

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Bruk os.path.join for å sette sammen stien
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'api', 'templates')],  # Korrekt sti
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n', 
            ],
        },
    },
]

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


ALLOWED_HOSTS = ['*']  # Tillat alle for lokal utvikling

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Sett standard auto-felt til BigAutoField


DEBUG = True

# Sett en unik SECRET_KEY for ditt lokale miljø
SECRET_KEY = 'your_generated_secret_key_here'  # Erstatt med din genererte hemmelige nøkkel

LOGIN_URL = 'login' 

AUTH_USER_MODEL = 'api.User'



LANGUAGE_CODE = 'nb'  # Norsk som standard

LANGUAGES = [
    ('nb', _('Norsk')),
    ('en', _('Engelsk')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

