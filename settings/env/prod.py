from settings.base import * 

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'