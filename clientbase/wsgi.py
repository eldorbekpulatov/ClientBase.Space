import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'clientbase.settings'

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise


application = get_wsgi_application()
application = WhiteNoise(application)