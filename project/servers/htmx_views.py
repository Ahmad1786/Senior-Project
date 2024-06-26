from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import EmailForm, SwapOfferForm, ServerForm
from posts.models import Bill, Event, Chore, SwapOffer, SwapRequest
from posts.group_page_forms import BillForm, EventForm, TaskForm, EditBillForm, EditEventForm, EditTaskForm, InvitationForm, AssignTaskForm, LeaderboardForm, CompleteTaskForm
from servers.models import Server, Participation, Invitation
from django.utils.timezone import get_current_timezone
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
                'server_id': server_id
            })
    
    form = TaskForm(server_instance=server_instance)
    return render(request, 'servers/partials/task-form.html', {
        'form': form,
        'server_id': server_id
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
                'form': form
                })
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


# Function to assign a task - done by Luke
def assign_task(request, task_id):
    assigned_task = Chore.objects.get(pk=task_id)
    if not is_htmx(request):
        return HttpResponse(status=405)
    if not can_edit(request.user, assigned_task):
        return HttpResponse(status=403)
    
    instance = Chore.objects.get(id=task_id)
    
    if request.method == 'POST':
        form = AssignTaskForm(request.POST, instance=instance)
        if form.is_valid():
            assigned_users = form.cleaned_data['assigned_users']
            assigned_task.assignee.set(assigned_users)
            assigned_task.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    else:
       form = AssignTaskForm(instance=instance)

    return render(request, 'servers/partials/assign-task-form.html', {
        'form': form,
    
    })     

#Function for joining a server
def join_server(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        invitation = Invitation.objects.filter(token=token).first()
        if invitation and invitation.expiration_time > timezone.now():
            server = invitation.server
            user = request.user
            display_name = f"{user.first_name} {user.last_name}"
            participation = Participation(user=user, server=server, display_name=display_name, is_owner=False)
            participation.save()

            #return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})

            return redirect('servers:server_page', server_id=server.id)

        else:
            messages.error(request, 'Invalid Invitation Code')

#Function to Create a server
@require_POST
def create_server(request):
    if request.method == 'POST':
        server_name = request.POST.get('name')
        if server_name:
            server = Server.objects.create(group_name=server_name)
            Participation.objects.create(user=request.user, server=server, is_owner=True)
            return redirect('servers:server_page', server_id=server.id)
        else:
            return HttpResponse(status=400)

def invitation(request, server_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    
    server_instance = Server.objects.get(pk=server_id)
    
    if request.method == 'GET':
        invitation = Invitation.create_invitation(server_instance)
        token = invitation.token
        expiration_time = invitation.expiration_time
        email_form = EmailForm()
        server_id=server_id
        # Render a modal showing the invitation token and expiration time
        return render(request, 'servers/partials/invitation-modal.html', {
            'token': token,
            'expiration_time': expiration_time,
            'email_form': email_form,
            'server_id': server_id
        })
    
    elif request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            emails = form.cleaned_data['emails'].split(',')
            response = Invitation.send_invitation_emails(server_instance, emails)
            return response
        else:
            return HttpResponse(status=400)  # Bad request if form is invalid
    
    return render(request, 'servers/partials/invitation-modal.html')


def close_modal(request):
    return HttpResponse('')

  
def reload_window(request):
    return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})

  
def leaderboard(request):
    if not is_htmx(request):
        return HttpResponse(status=405)

    if request.method == 'POST':
        form = LeaderboardForm(request.POST)
    else:
        form = LeaderboardForm()

    return render(request, 'servers/partials/leaderboard.html', {'form': form})


def mark_as_complete(request, task_id):
    task = Chore.objects.get(pk=task_id)
    context = {
        "chore": task
    }
    
    if request.method == 'POST':
        user = request.user
        task.mark_as_complete(request.user)
        server = task.server
        participation = Participation.objects.get(server=server, user = request.user)
        participation.points += task.point_val
        participation.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    
    return render(request, 'servers/partials/complete-task-modal.html', context=context)

def mark_as_paid(request, bill_id):
    bill = Bill.objects.get(pk=bill_id)
    context = {
        "bill": bill
    }

    if request.method == 'POST':
        user = request.user
        bill.mark_as_paid(request.user)
        return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    
    return render(request, 'servers/partials/mark-as-paid-modal.html', context=context)

def delete_post(request, post_type, post_id):
    if request.method == 'POST':
        if post_type == "bill":
            bill = Bill.objects.get(pk=post_id)
            bill.delete()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        if post_type == "event":
            event = Event.objects.get(pk=post_id)
            event.delete()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        if post_type == "chore":
            chore = Chore.objects.get(pk=post_id)
            chore.delete()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    
    return render(request, 'servers/partials/confirm-deletion.html')
        
        
        