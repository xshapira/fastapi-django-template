from django.contrib import admin

from users.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    search_fields = ("name", "email")
    list_display = ("id", "name", "email")
    ordering = ("id",)
