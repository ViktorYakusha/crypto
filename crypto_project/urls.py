import os
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

from crypto_project.main import views as main_views
from crypto_project.customer import views as customer_views, consumers


urlpatterns = [
    path('login', customer_views.customer_login, name='customer_login'),
    path('logout', customer_views.customer_logout, name='customer_logout'),
    path('profile/', customer_views.customer_profile, name='customer_profile'),
    path('profile/account', customer_views.customer_profile_account, name='customer_profile_account'),
    path('profile/bills', customer_views.customer_profile_bills, name='customer_profile_bills'),
    path('profile/settings', customer_views.customer_profile_settings, name='customer_profile_settings'),
    path('profile/load-open-bets', customer_views.customer_load_open_bets, name='customer_load_open_bets'),
    path('profile/load-close-bets', customer_views.customer_load_close_bets, name='customer_load_close_bets'),
    path('profile/load-payments', customer_views.customer_load_payments, name='customer_load_payments'),
    path('registration', customer_views.customer_registration, name='customer_registration'),
    path('create-bet', customer_views.customer_create_bet, name='customer_create_bet'),

    path('', main_views.homepage, name='homepage'),
    path(os.getenv('ADMIN_URL'), admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()
