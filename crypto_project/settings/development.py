import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = True
INTERNAL_IPS = os.getenv('DJANGO_INTERNAL_IPS', '').split(',')

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'debug_toolbar',
    'authtools',
    'django_celery_results',
    'django_celery_beat',
    'phonenumber_field',
    'crypto_project.customer',
    'crypto_project.main',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files/')