import os, site
from os.path import abspath, dirname, join
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "futurice_checklist.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
