
from pathlib import Path
import os
import traceback

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print('BASE_DIR=', BASE_DIR)

# Application definition

INSTALLED_APPS = [
    'account',
    'mainapp',
    'parser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    #'drf_spectacular',
    'corsheaders',
    #'graphene_django',
    'captcha',
    'djoser',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ['https://images.freebello.com',
                        'https://beta.images.freebello.com',
                        'https://alpha.images.freebello.com',
                        'https://cdn.freebello.com/',
                        'https://img.freebello.com/',
                        'https://storage.yandexcloud.net/'
                        ]


ROOT_URLCONF = 'freebello.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
  
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'SEND_CONFIRMATION_EMAIL':True,
    'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND':True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND':True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION':True,
    'SERIALIZERS': {
        'current_user': 'mainapp.serializers.SpecialUserSerializer',
    },
    'EMAIL': {
        'password_reset': 'mainapp.email.PasswordResetEmail',
    },
}





TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.request']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'freebello.wsgi.application'
AUTH_USER_MODEL = 'account.User'


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/



# IP = '62.113.104.27'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Freebello',
    'DESCRIPTION': 'API v1',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


GRAPHENE = {
    'SCHEMA': 'gql.schema',
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'










try:
    from .local_settings import *

except ImportError:
    from .product_settings import *
