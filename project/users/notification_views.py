from django.shortcuts import render
from users.models import Notification, User
from django.http import HttpResponse
from django.shortcuts import redirect

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
    return redirect('users:notification_page')