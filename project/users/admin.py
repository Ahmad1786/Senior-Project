from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
# (Can configure later as well)

admin.site.register(User, UserAdmin)
