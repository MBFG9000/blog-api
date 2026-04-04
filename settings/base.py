# Python modules
from os import path

# Django settings
from django.utils.translation import gettext_lazy as _

# Project modules 
from settings.conf import *



# -----------------------------------------------------------
# Path
#
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
ROOT_URLCONF = 'settings.urls'
WSGI_APPLICATION = 'settings.wsgi.application'
AUTH_USER_MODEL = "users.CustomUser"
HOME_PAGE_URL = 'http://localhost:8000/posts'

# -----------------------------------------------------------
# Apps
#
DJANGO_AND_THIRD_PARTY_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
]
PROJECT_APPS = [
    'apps.abstracts.apps.AbstractsConfig',
    'apps.users.apps.UsersConfig',
    'apps.blog.apps.BlogConfig',
]
INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS

# -----------------------------------------------------------
# Middleware | Templates | Validators
#
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.abstracts.middlewares.UserLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -----------------------------------------------------------
# Internationalization
# 
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
    ('kk', _('Kazakh')),
)

DEFAULT_LANGUAGE_CODE = LANGUAGES[0][0]

# -----------------------------------------------------------
# Static | Media
# 
STATIC_URL = "static/"
STATIC_ROOT = path.join(BASE_DIR, 'static')
MEDIA_URL = "media/"
MEDIA_ROOT = path.join(BASE_DIR, 'media')

LOCALE_PATHS = [
    path.join(BASE_DIR, 'locale/')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------
# Email 
# 

from os import getenv # just for testing

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = '' 
EMAIL_USE_TLS = True