# Python modules
import os

# Django modules
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Project modules
from settings.conf import ENV_ID, ENV_POSSIBLE_OPTIONS
from apps.notifications.routing import websocket_urlpatterns

assert ENV_ID in ENV_POSSIBLE_OPTIONS, f"Invalid env id. Possible options{ENV_POSSIBLE_OPTIONS}"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"settings.env.{ENV_ID}")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))  
    }
)
