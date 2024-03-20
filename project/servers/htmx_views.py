from django.shortcuts import render
from django.http import HttpResponse
from posts.group_page_forms import BillForm, EventForm, TaskForm
from posts.models import Bill, Event, Chore
from servers.models import Server

# These views will be used to create the modal forms that pop up
# in the main group page to create a new post

def add_bill(request, server_id):
    server_instance = Server.objects.get(pk=server_id)
    current_user = request.user
    if request.method == 'POST':
        form = BillForm(request.POST, server_instance=server_instance, current_user=current_user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.server = server_instance
            obj.creator = request.user
            obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'NewPostAdded'})
        else:
            return render(request, 'servers/partials/bill-form.html', {
                'form': form,
            })
    
    form = BillForm(server_instance=server_instance, current_user=current_user)
    return render(request, 'servers/partials/bill-form.html', {
        'form': form,
    })


def add_task(request, server_id):
    server_instance = Server.objects.get(pk=server_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, server_instance=server_instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.server = server_instance
            obj.creator = request.user
            obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'NewPostAdded'})
        else:
            return render(request, 'servers/partials/task-form.html', {
                'form': form,
            })
    
    form = TaskForm(server_instance=server_instance)
    return render(request, 'servers/partials/task-form.html', {
        'form': form,
    })


def add_event(request, server_id):
    server_instance = Server.objects.get(pk=server_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.server = server_instance
            obj.creator = request.user
            obj.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'NewPostAdded'})
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
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EditEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'Event Updated'})
    else:
        form = EditEventForm(instance=event)
    return render(request, 'servers/partials/edit-event-form.html', {'form': form})

# Function to edit bill - done by Luke
def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        form = EditBillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'Bill Updated'})
    else:
        form = EditBillForm(instance=bill)
    return render(request, 'servers/partials/edit-bill-form.html', {'form': form})

# Function to edit task - done by Luke
def edit_task(request, task_id):
    task = get_object_or_404(Chore, id=task_id)
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'Task Updated'})
    else:
        form = EditTaskForm(instance=task)
    return render(request, 'servers/partials/edit-task-form.html', {'form': form})
