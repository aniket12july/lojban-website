
import os, sys
from os.path import join, dirname, normpath

sys.path.append(normpath(join(dirname(__file__), '..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'lojban.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
