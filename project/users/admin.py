from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from servers.admin import ParticipationInline
from posts.models import Chore, Bill, Event

User = get_user_model()

class ChoreInline(admin.TabularInline):
    model = Chore
    extra = 1
class BillInline(admin.TabularInline):
    model = Bill
    extra = 1
class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    
class MyUserAdmin(UserAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = ('id',) + self.list_display + ('phone_number',) + ('profile_picture',)
        next(field_option for name, field_option in self.fieldsets if name == 'Personal info')['fields'] += ('phone_number',)
        next(field_option for name, field_option in self.fieldsets if name == 'Personal info')['fields'] += ('profile_picture',)

    inlines = [ParticipationInline, ChoreInline, BillInline, EventInline] 


# Register models
admin.site.register(User, MyUserAdmin)
