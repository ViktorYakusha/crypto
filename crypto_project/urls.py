from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from .apps.main import views as main_views

urlpatterns = [
    path('', main_views.homepage),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + debug_toolbar_urls()
