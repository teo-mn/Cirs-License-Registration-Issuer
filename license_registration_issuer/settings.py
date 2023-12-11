"""
Django settings for license_registration_issuer project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

DEBUG = env.get_value('DEBUG', bool, False)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value('SECRET_KEY', str, 'django-insecure-b6%@==j2_fn&mga5b!=u*u$6y@7*as&d5tw1!8ue*lp_x=*c0p')
# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', list, ['*'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', list, [])

# CORS
# CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', list, ['*'])
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', list, ['*'])
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'license_registration_issuer',
    'django_celery_beat',
    'graphene_django',
    'corsheaders',
    'syncer'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'license_registration_issuer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'license_registration_issuer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.get_value('DB_ENGINE', str, 'django.db.backends.sqlite3'),
        'NAME': env.get_value('DB_NAME', str, 'db.sqlite3'),
        'USER': env.get_value('DB_USER', str, ''),
        'PASSWORD': env.get_value('DB_PASSWORD', str, ''),
        'HOST': env.get_value('DB_HOST', str, ''),
        'PORT': env.get_value('DB_PORT', str, '')
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_ROOT = os.path.join(CONTENT_DIR, 'static')
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s][%(name)s] [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {}
}

# celery
CELERY_TIMEZONE = "Asia/Ulaanbaatar"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERYD_CONCURRENCY = 1
CELERY_WORKER_CONCURRENCY = 1
CELERY_BROKER_URL = env.get_value('CELERY_BROKER_URL', str, 'amqp://guest:guest@localhost:5672')

CELERY_TASK_DEFAULT_EXCHANGE = env.get_value('CELERY_TASK_DEFAULT_EXCHANGE', str, 'cirs_exchange')
CELERY_TASK_DEFAULT_ROUTING_KEY = env.get_value('CELERY_TASK_DEFAULT_ROUTING_KEY', str, 'cirs_key')
CELERY_TASK_DEFAULT_QUEUE = env.get_value('CELERY_TASK_DEFAULT_QUEUE', str, 'cirs_queue')
SYNCER_CRON_JOB_MINUTE = env.get_value('SYNCER_CRON_JOB_MINUTE', str, '*/3')
SYNCER_ON = env.get_value('SYNCER_ON', bool, False)

# blockchain
NODE_URL = env.get_value('NODE_URL', str, 'https://node-testnet.corexchain.io')
NODE_URL_WS = env.get_value('NODE_URL_WS', str, 'ws://157.245.49.81:18546')  # ws://34.124.146.188:18546
CHAIN_ID = env.get_value('CHAIN_ID', int, 3305)
PRODUCT_ADDRESS = env.get_value('PRODUCT_ADDRESS', str, '0xD5a6036f145689A857270a5154Dfd731D6795375')
KV_ADDRESS = env.get_value('KV_ADDRESS', str, '0xe5CA73D03774b1be632FF70832176B24c183EB0a')
LICENSE_REGISTRATION_ADDRESS = env.get_value('LICENSE_REGISTRATION_ADDRESS', str,
                                             '0x51Dd1F5340BEE46C6d28262204FEA469C55205E5')
REQUIREMENT_REGISTRATION_ADDRESS = env.get_value('REQUIREMENT_REGISTRATION_ADDRESS', str,
                                                 '0x393eB5AA172a2aE6FD60225B139158b183fa23c8')
GAS_FEE_GWEI = env.get_value('GAS_FEE_GWEI', int, 700)
DEFAULT_GAS_LIMIT = env.get_value('DEFAULT_GAS_LIMIT', int, 2000000)
ISSUER_ADDRESS = env.get_value('ISSUER_ADDRESS', str, '0x85F5c799e1edEe7Fc042638D5c00da3a5cC8c7a4')
ISSUER_PK = env.get_value('ISSUER_PK', str, '')

# graphql
GRAPHENE = {
    "SCHEMA": "syncer.schema.schema"
}
