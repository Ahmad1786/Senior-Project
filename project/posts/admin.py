from django.contrib import admin
from .models import Event, Bill, Chore, Comment

# Can also do some configurations

# Register your models here.
admin.site.register(Event)
admin.site.register(Bill)
admin.site.register(Chore)
admin.site.register(Comment)