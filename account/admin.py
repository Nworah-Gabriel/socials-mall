from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    list_filter = ("username", "email")
    # readonly_fields = ["balance"]

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)