from django.contrib import admin

from .models import Customer, Manager, Comment


class CustomerAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ['user__name', 'user__email', 'manager__user__name', 'balance', 'is_verified']
    list_filter = ['manager__user__name']

admin.site.register(Customer, CustomerAdmin)


class ManagerAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ['user__name', 'user__email']

admin.site.register(Manager, ManagerAdmin)


class CommentAdmin(admin.ModelAdmin):
    exclude = ('customer', 'author',)
    list_display = ['customer__user__name', 'author__user__name', 'created_date']
    list_filter = ['customer__user__name', 'author__user__name']

admin.site.register(Comment, CommentAdmin)