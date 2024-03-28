from django.contrib import admin
from .models import Server, Participation, Invitation

# essentially simulates filter_horizontal but for relationships with bridging tables
class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1

class ServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name', 'date_created')
    inlines = [ParticipationInline]

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'points', 'date_joined', 'is_owner', 'server_name')
    
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('token', 'server', 'invited_email', 'invited_user', 'expiration_time')

# Register models
admin.site.register(Server, ServerAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(Invitation, InvitationAdmin)
