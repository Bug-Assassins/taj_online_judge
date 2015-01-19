"""
Django settings for TAJ project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# File Created by Ashish Kedia, ashish1294@gmail.com
# Created on 6th Jan, 2015
# Last Modified on 15th Jan, 2015

'''Happiness is always a choice you have. Happiness is sharing. Even with a
pet or a plant or a headphone. Happiness is easy. It's just a change of mind.
You don't need solitude to be happy, all you need is a sense of good choice'''

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(os.path.join(os.path.abspath(os.path.join(SITE_ROOT, os.pardir)),'taj_app/'),'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_e(iigozjj6(8wf*vo6$oh4zf&ft-jhickf73&ir8&-f69wy#+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taj_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.join(os.path.join(SITE_ROOT, '..'),'taj_app'),'template'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'TAJ.urls'

WSGI_APPLICATION = 'TAJ.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taj',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3308',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = os.path.join(os.path.join(os.path.abspath(os.path.join(PROJECT_PATH, os.pardir)),'taj_app/'),'files/')

STATICFILES_DIRS = (
    os.path.join(os.path.join(os.path.abspath(os.path.join(PROJECT_PATH, os.pardir)),'taj_app'),'files'),
)

# USER CODE STORAGE SETTINGS
TESTCASE_DIR = '/home/ashish/Desktop'
SUBMISSION_DIR = '/home/ashish/Desktop'
TEMP_FILE_PATH = '/home/ashish/Desktop'