from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    fields = ["user"]


admin.site.register(Customer)