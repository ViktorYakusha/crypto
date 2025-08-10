import os
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from .apps.main import views as main_views
from .apps.customer import views as customer_views

urlpatterns = [
    path('', main_views.homepage),
    path('registration', customer_views.registration, name='customer_registration'),
    path(os.getenv('ADMIN_URL'), admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + debug_toolbar_urls()
