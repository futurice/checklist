import django.conf.global_settings as DEFAULT_SETTINGS
import os
PACKAGE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_ROOT = os.path.normpath(PACKAGE_ROOT)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f0$5!!_^+roj!^nru@@%9eku33-%miucnd-ekczegyph9&v*(d'

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

    'common',
    'employee',
    'editlist',
    'reminders',
    #'south',
    #'raven.contrib.django',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'futurice_checklist.urls'

WSGI_APPLICATION = 'futurice_checklist.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'data.sqlite'),
    }
}

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/'),
)
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS +\
('employee.context_processors.get_userinfo', 'employee.context_processors.get_reminders',)

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
#SENTRY_KEY = 'js52wjdsoisr78fgs1f0g415safg1'
#SENTRY_SERVERS = ['https://sentry.futurice.com/sentry/store/']
