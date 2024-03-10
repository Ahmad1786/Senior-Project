from django.contrib import admin
from .models import Server, Participation

# essentially simulates filter_horizontal but for relationships with bridging tables
class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1

class ServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name', 'date_created')
    inlines = [ParticipationInline]

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'points', 'date_joined', 'is_owner')

# Register models
admin.site.register(Server, ServerAdmin)
admin.site.register(Participation, ParticipationAdmin)
