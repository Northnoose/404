import os
from django.core.wsgi import get_wsgi_application

# This tells Django where to find your settings file.
# It assumes your settings are in 'config.settings'
# (i.e., backend/config/settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()