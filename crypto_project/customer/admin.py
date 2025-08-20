from django.contrib import admin

from .models import Customer, Manager


class CustomerAdmin(admin.ModelAdmin):
    fields = ["user", "first_name", "last_name", "email"]


admin.site.register(Customer)


class ManagerAdmin(admin.ModelAdmin):
    fields = ["user", "first_name", "last_name", "email"]


admin.site.register(Manager)