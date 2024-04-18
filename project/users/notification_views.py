from django.shortcuts import render
from users.models import Notification, User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def notification_page(request):
    notifications = request.user.notifications.order_by('-created').all()
    return render(request, 'users/notifications.html', {'notifications': notifications})

def unread_notification_count(request):
    user = User.objects.get(pk=request.user.id)
    c = user.notifications.filter(read=False).count()
    return HttpResponse(c)

def mark_as_read(request, notification_id):
    n = Notification.objects.get(pk=notification_id)
    n.read = True
    n.save()
    return render(request, 'users/notification_item.html', {'n': n})