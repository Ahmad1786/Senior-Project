from django.shortcuts import render
from django.http import HttpResponse
from posts.group_page_forms import BillForm


# These views will be used to create the modal forms
# that pop up in the main group page to create a new post

def add_bill(request, server_id):
    if request.method == 'POST':
        form = BillForm(request.POST, request=request, current_server_id=server_id)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'billListChanged'})
        else:
            return render(request, 'servers/partials/bill-form.html', {
                'form': form,
            })
    
    form = BillForm(request=request, current_server_id=server_id)
    return render(request, 'servers/partials/bill-form.html', {
        'form': form,
    })

def add_task(request, server_id):
    return HttpResponse(f"Adding a task for server {server_id}!")

def add_event(request, server_id):
    return HttpResponse(f"Adding an event for server {server_id}!")