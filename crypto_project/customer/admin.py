from django.contrib import admin

from .models import Customer, Manager, Comment


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user__name", "user__email", "manager__user__name", "balance", "is_verified"]

admin.site.register(Customer, CustomerAdmin)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ["user__name", "user__email"]

admin.site.register(Manager, ManagerAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['customer__user__name', 'author__user__name', 'created_date']

admin.site.register(Comment, CommentAdmin)