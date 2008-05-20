
from settings_local import *

ADMINS = (
# Don't uncomment until somebody is reading this mailbox!
#    ('Lojban Webmaster', 'webmaster@lojban.com'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'webmaster@lojban.com'
SERVER_EMAIL = 'webmaster@lojban.com'
EMAIL_SUBJECT_PREFIX = '[Lojban website] '
SEND_BROKEN_LINK_EMAILS=True

SESSION_SAVE_EVERY_REQUEST=True

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en'
USE_I18N = False

ADMIN_MEDIA_PREFIX = '/admin-media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'lojban.urls'

TEMPLATE_DIRS = (
    join(LOCAL_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.humanize',
    'lojban.main',
)

