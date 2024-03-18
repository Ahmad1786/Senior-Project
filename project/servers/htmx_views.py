from django.shortcuts import render
from django.http import HttpResponse
from posts.group_page_forms import BillForm, EventForm, TaskForm


# These views will be used to create the modal forms that pop up
# in the main group page to create a new post

def add_bill(request, server_id):
    if request.method == 'POST':
        form = BillForm(request.POST, request=request, current_server_id=server_id)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'NewPostAdded'})
        else:
            return render(request, 'servers/partials/bill-form.html', {
                'form': form,
            })
    
    form = BillForm(request=request, current_server_id=server_id)
    return render(request, 'servers/partials/bill-form.html', {
        'form': form,
    })


def add_task(request, server_id):
    if request.method == 'POST':
        form = TaskForm(request.POST, request=request, current_server_id=server_id)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'NewPostAdded'})
        else:
            return render(request, 'servers/partials/task-form.html', {
                'form': form,
            })
    
    form = TaskForm(request=request, current_server_id=server_id)
    return render(request, 'servers/partials/task-form.html', {
        'form': form,
    })


def add_event(request, server_id):
    if request.method == 'POST':
        form = EventForm(request.POST, request=request, current_server_id=server_id)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'NewPostAdded'})
        else:
            return render(request, 'servers/partials/event-form.html', {
                'form': form,
            })
    
    form = EventForm(request=request, current_server_id=server_id)
    return render(request, 'servers/partials/event-form.html', {
        'form': form,
    })