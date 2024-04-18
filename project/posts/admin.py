from django.contrib import admin
from .models import Event, Bill, Chore, Comment, RecurringTask, PostImage

# Configurations - These give more control in the admin panel
# list_display - what fields show up admin panel
# filter_horizontal - allows viewing and controling many-to-many relationship instances
# inlines - similar result as filter_horizontal but for one-to-many relationship instances

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class ImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_name', 'creator', 'server', 'date_created', 'date_time')
    inlines = (CommentInline,)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_name', 'cost', 'split', 'bill_creator', 'server', 'posted_date')
    inlines = (CommentInline,)
    filter_horizontal = ('payers',)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_name', 'completed', 'assigner', 'server', 'assigned_date')
    inlines = (CommentInline, ImageInline,)
    filter_horizontal = ('assignee',)

class ReplyInline(admin.TabularInline):
    model = Comment
    extra = 1
class CommentAdmin(admin.ModelAdmin):
    # filter_horizontal = ('events', 'bills', 'chores')
    list_display = ('id', 'author', 'post', 'date_time', 'parent_comment')
    inlines = (ReplyInline,)

    def post(self, obj):
        return obj.task or obj.event or obj.bill

class RecurringTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'server', 'creator', 'due_date')
    filter_horizontal = ('assignee',)

# Register models
admin.site.register(Event, EventAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Chore, ChoreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(RecurringTask, RecurringTaskAdmin)