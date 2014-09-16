"""
Django settings for requirejs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import dirname, abspath

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_PATH = dirname(abspath(__file__))
DJANGO_PROJECT_PATH = BASE_DIR
PROJECT_PATH = dirname(DJANGO_PROJECT_PATH)


def django_project_path_join(path):
    return os.path.join(DJANGO_PROJECT_PATH, path)


def project_path_join(path):
    return os.path.join(PROJECT_PATH, path)


def settings_path_join(path):
    return os.path.join(SETTINGS_PATH, path)


def deduce(name, glob):
    execfile(settings_path_join('deduce_%s.py' % name), glob)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1jts7^=k#!$g=p19r7k+(%46d&zli(smbv7$=%8umciy!e$r(l'

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
    'compressor',
    'mainapp',
    'django.contrib.admin',
    'compressor_requirejs'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'requirejs.urls'

WSGI_APPLICATION = 'requirejs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

#
# print STATICFILES_DIRS

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_ROOT = django_project_path_join('collected-static')
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

COMPRESS_ENABLED = True

COMPRESS_CSS_HASHING_METHOD = 'content'

COMPRESS_PRECOMPILERS = (
    ('text/requirejs', 'compressor_requirejs.compressor.r_precompiler.RequireJSPrecompiler'),
)

COMPRESS_JS_FILTERS = [
    'mainapp.compressor_filters.template.TemplateFilter'
]


COMPRESS_PARSER = 'compressor.parser.HtmlParser'

COMPRESSOR_REQUIREJS_TMP = django_project_path_join('tmp')

COMPRESSOR_REQUIREJS_REQUIRED_LIBS = {
    'jquery': 'mainapp/js/libs/jquery-2.1.0.min.js'
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
         'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'mainapp.custom': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
}


def logging_compressor_requirejs(text):
    import logging
    logger = logging.getLogger('mainapp.custom')
    logger.debug(text)

COMPRESSOR_REQUIREJS_LOGGING_OUTPUT_FUNCTION = logging_compressor_requirejs
