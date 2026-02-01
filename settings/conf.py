# Project modules
from decouple import config

# -------------------------------
# Env id
#

ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)
ENV_ID = config("DJANGO_ADV_ENV_ID", cast=str)
SECRET_KEY = 'django-insecure-c566qv-369ufrzn-_5!jf^b-7b^3*nn3#dh_pfg#phq*k93t$b'

# -------------------------------
# NAME
#