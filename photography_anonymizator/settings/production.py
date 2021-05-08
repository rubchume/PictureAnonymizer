# In a production environment, the next environment variable must be set:
# DJANGO_SETTINGS_MODULE=photography_anonymizator.settings.production

import django_heroku

from .base import *

ALLOWED_HOSTS = ['.herokuapp.com']


# Activate Django-Heroku.
django_heroku.settings(locals())
