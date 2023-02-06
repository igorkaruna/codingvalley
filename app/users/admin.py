from django.contrib import admin

from users.models import User


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_per_page = 10
