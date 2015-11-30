import django.conf.global_settings as DEFAULT_SETTINGS
import os
PACKAGE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_ROOT = os.path.normpath(PACKAGE_ROOT)

SECRET_KEY = os.getenv('SECRET_KEY', '')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
TEMPLATE_DEBUG = os.getenv('TEMPLATE_DEBUG', 'false').lower() == 'true'
allowed_hosts = os.getenv('ALLOWED_HOSTS', '*')
ALLOWED_HOSTS = allowed_hosts.split(',')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'common',
    'employee',
    'editlist',
    'reminders',

    'django_extensions',
    #'south',
    #'raven.contrib.django',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',
    'futurice_checklist.auth.CustomHeaderMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
)

ROOT_URLCONF = 'futurice_checklist.urls'
WSGI_APPLICATION = 'wsgi.application'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DB_TYPE = os.getenv('DB_TYPE', 'default')

if DB_TYPE == 'default':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_ROOT, 'data.sqlite'),
        }
    }
else:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': os.getenv('DB_NAME', 'checklist'),                      # Or path to database file if using sqlite3.
                # The following settings are not used with sqlite3:
                'USER': os.getenv('DB_USER', 'checklist'),
                'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
                'HOST': os.getenv('DB_HOST', 'localhost'),                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
                'PORT': os.getenv('DB_PORT', '5432'),                      # Set to empty string for default.
            }
        }

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/'),
)
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'employee.context_processors.get_userinfo',
    'employee.context_processors.get_reminders',
    'employee.context_processors.get_checklists',
    'common.context_processors.cdn',
    )

CDN_URL = 'https://cdn.futurice.com/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


MEDIA_ROOT = '{PROJECT_ROOT}/media/'.format(**locals())
MEDIA_URL = '/media/'

STATIC_ROOT = '{PROJECT_ROOT}/static/'.format(**locals())
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = DEFAULT_SETTINGS.STATICFILES_FINDERS

#SENTRY_TESTING = True
#SENTRY_KEY = ''
#SENTRY_SERVERS = ['']

try:
    # secrets here; needs to be somewhere in PYTHONPATH (eg. project-root, user-root)
    from local_settings import *
except Exception, e:
    print "No local_settings configured, ignoring..."
