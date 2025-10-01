from .base import *

ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'production')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *