from django.shortcuts import render
from django.http import HttpResponse
from posts.group_page_forms import BillForm, EventForm, TaskForm, EditBillForm, EditEventForm, EditTaskForm
from posts.models import Bill, Event, Chore
from servers.models import Server
from django.utils.timezone import get_current_timezone

# some quick server side validation
# was trying to see if I could use a decorator for ease but those are complicated
is_htmx = lambda request: request.headers.get('HX-Request', False)
can_edit = lambda user, post: user == post.creator

# These views will be used to create the modal forms that pop up
# in the main group page to create a new post
def add_bill(request, server_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    server_instance = Server.objects.get(pk=server_id)
    current_user = request.user
    if request.method == 'POST':
        form = BillForm(request.POST, server_instance=server_instance, current_user=current_user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.server = server_instance
            obj.creator = request.user
            obj.save()
            form.save_m2m()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            return render(request, 'servers/partials/bill-form.html', {
                'form': form,
            })
    
    form = BillForm(server_instance=server_instance, current_user=current_user)
    return render(request, 'servers/partials/bill-form.html', {
        'form': form,
    })


def add_task(request, server_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    server_instance = Server.objects.get(pk=server_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, server_instance=server_instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.server = server_instance
            obj.creator = request.user
            obj.save()
            form.save_m2m()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            return render(request, 'servers/partials/task-form.html', {
                'form': form,
            })
    
    form = TaskForm(server_instance=server_instance)
    return render(request, 'servers/partials/task-form.html', {
        'form': form,
    })


def add_event(request, server_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    server_instance = Server.objects.get(pk=server_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.server = server_instance
            obj.creator = request.user
            obj.save()
            form.save_m2m()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            return render(request, 'servers/partials/event-form.html', {
                'form': form,
            })
    
    form = EventForm()
    return render(request, 'servers/partials/event-form.html', {
        'form': form,
    })

# Function to edit event - done by Luke
def edit_event(request, event_id):
    instance = Event.objects.get(id=event_id)
    
    if not is_htmx(request):
        return HttpResponse(status=405)
    if not can_edit(request.user, instance):
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        form = EditEventForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    else:
        # get the time but in our timezone
        date_time = instance.date_time.astimezone(get_current_timezone())
        
        # format it as needed to show up in the form calendar view
        formatted_datetime = date_time.strftime("%Y-%m-%dT%H:%M")
        
        return render(request, 'servers/partials/edit-event-form.html', {
            'form': EditEventForm(instance=instance, initial={'date_time': formatted_datetime})
            })

# Function to edit bill - done by Luke
def edit_bill(request, bill_id):
    instance = Bill.objects.get(id=bill_id)
    
    if not is_htmx(request):
        return HttpResponse(status=405)
    if not can_edit(request.user, instance):
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        form = EditBillForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    else:
        return render(request, 'servers/partials/edit-bill-form.html', {
            'form': EditBillForm(instance=instance)
            })

# Function to edit task - done by Luke
def edit_task(request, task_id):
    instance = Chore.objects.get(id=task_id)
    
    if not is_htmx(request):
        return HttpResponse(status=405)
    if not can_edit(request.user, instance):
        return HttpResponse(status=403)
    
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    else:
        return render(request, 'servers/partials/edit-task-form.html', {
            'form':  EditTaskForm(instance=instance)
            })

