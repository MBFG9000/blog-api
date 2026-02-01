# Python modules
import os

# Django modules
from django.core.wsgi import get_wsgi_application

# Project module
from settings.conf import ENV_ID, ENV_POSSIBLE_OPTIONS


assert ENV_ID in ENV_POSSIBLE_OPTIONS, f"Invalid ENV_ID. Possible options: {ENV_POSSIBLE_OPTIONS}"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"settings.env.{ENV_ID}")

application = get_wsgi_application()
