# In a production environment, the next environment variable must be set:
# DJANGO_SETTINGS_MODULE=photography_anonymizator.settings.production

from .base import *


ALLOWED_HOSTS = ['.herokuapp.com']
