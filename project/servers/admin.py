from django.contrib import admin
from .models import Server, Participation

# Can also do some configurations

# Register your models here.
admin.site.register(Server)
admin.site.register(Participation)
