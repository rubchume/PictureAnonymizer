# In a production environment, the next environment variable must be set:
# DJANGO_SETTINGS_MODULE=photography_anonymizator.settings.production
import dj_database_url
import django_heroku

from .base import *


ALLOWED_HOSTS = ['.herokuapp.com']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'photography_anonymyzer',
        'USER': 'name',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())
