"""
Django settings for cronProjectAPI project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dj_database_url
# from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'ps7(e&!!l(kbsmr$76qia@(zi%p=^w-r=(+()ex!33*pyd*8x^'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'ps7(e&!!l(kbsmr$76qia@(zi%p=^w-r=(+()ex!33*pyd*8x^')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )

ALLOWED_HOSTS = [
    'mein-r1an-frau.herokuapp.com',
    'delivery-api-cron.herokuapp.com',
    '127.0.0.1',
    'localhost'
]

# Application definition

INSTALLED_APPS = [
    'catalog.apps.CatalogConfig',
    'feedbacks.apps.FeedbacksConfig', 
    'nested_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'rest_framework.authtoken',
    'django_filters',
    'accounts',
    'knox',
    'orders',

    # 'fcm_django'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated'
    # ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cronProjectAPI.urls'


AUTHENTICATION_BACKENDS = [
    # 'accounts.auth_backend.PasswordlessAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
    ]

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

WSGI_APPLICATION = 'cronProjectAPI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'crondelivery',
        'USER' : 'cronadmin',
        'PASSWORD' : 'cronDelivery_1804',
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
        }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Twilio
# TWILIO_PHONE = config('TWILIO_PHONE', default = None)
# TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default=None)
# TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default = None)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'accounts.User'

from datetime import timedelta

REST_KNOX = {
    'USER_SERIALIZER': 'accounts.serializers.UserSerializer',
    'TOKEN_TTL': timedelta(hours= 24*60),
}

'''
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY" "[AAAAL9hLaRs:APA91bEguNRPUIZGwUAS-0YIirqQqlZRYVsUyO4dWfr0zC2b-EgV57qrqFd_i16HsTTcOB-t6z8pfa4YElC-qfD-AzPKlzoSmlx_MH3yGOmGcRspSUlw9zyQZjEccGhzZF83BP4_vYnZ]"
}'''


ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'