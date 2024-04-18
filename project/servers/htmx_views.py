from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from posts.group_page_forms import BillForm, EventForm, TaskForm, EditBillForm, EditEventForm, EditTaskForm, InvitationForm, AssignTaskForm
from .forms import EmailForm, SwapOfferForm
from posts.models import Bill, Event, Chore, SwapOffer, SwapRequest
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


# Function to assign a task - done by Luke
def assign_task(request):
    if not is_htmx(request):
        return HttpResponse(status=405)
    tasks_to_assign = Chore.objects.filter(assigned_date__isnull=True)

    if request.method == 'POST':
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            assigned_task_id = form.cleaned_data['task_id']
            assigned_users = form.cleaned_data['assigned_users']
            assigned_task = Chore.objects.get(pk=assigned_task_id)
            assigned_task.assignee.set(assigned_users)
            
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
    else:
        form = AssignTaskForm()

    context = {
        'form': form,
        'tasks_to_assign': tasks_to_assign,
    }
    return render(request, 'servers/partials/assign-task-form.html', context)

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
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            messages.error(request, 'Invalid Invitation Code')

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


def swap_request(request, task_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    
    chore_instance = Chore.objects.get(pk=task_id)
    context = {
        "chore": chore_instance
    }
    
    if request.method == 'POST':
        SwapRequest.create_swap_request(chore_instance, request.user)
        context['success'] = True
    
    return render(request, 'servers/partials/swap-request-modal.html', context=context)

@require_POST
def create_swap_offer(request, swap_request_id):
    swap_request = SwapRequest.objects.get(pk=swap_request_id)
    form = SwapOfferForm(request.POST, user=request.user, swap_request=swap_request)
    request_server = swap_request.chore.server
    all_swap_requests = SwapRequest.objects.filter(chore=swap_request.chore, status='PENDING').exclude(id=swap_request_id)
    if form.is_valid():
        # Extract form data
        offer_chore = form.cleaned_data['offer_chore']
        status = form.cleaned_data['status']
        # Create the swap offer
        
        if status == 'ACCEPTED' or status == 'Accepted' and offer_chore != None:
            SwapOffer.create_offer(swap_request=swap_request, offer_chore=offer_chore, status=status, user=request.user)
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        elif status == 'ACCEPTED' or status == 'Accepted' and offer_chore==None:
            SwapOffer.create_offer(swap_request=swap_request, offer_chore=offer_chore, status=status, user=request.user)
            for swap_request_left in all_swap_requests:
                SwapOffer.create_offer(swap_request=swap_request_left, offer_chore=None, status="DECLINED", user=request.user)
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        elif status == 'DECLINED' or status == 'Declined':
            SwapOffer.create_offer(swap_request=swap_request_left, offer_chore=None, status="DECLINED", user=request.user)
        else:
            SwapOffer.create_offer(swap_request=swap_request_left, offer_chore=None, status="PENDING", user=request.user)
        return JsonResponse({'status': 'success'}, status=200)

def manage_swap_request(request, swap_request_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    
    swap_request_instance = SwapRequest.objects.get(pk=swap_request_id)
    print(swap_request_instance)
    swap_request_offers = SwapOffer.objects.filter(swap_request=swap_request_instance)
    
    if request.method == 'POST':
        if 'accept_swap_offer' in request.POST:
            offer_id = request.POST.get('accept_swap_offer')
            offer = SwapOffer.objects.get(pk=offer_id)
            offer.accept_offer()
            return HttpResponse(status=204)
        elif 'decline_swap_offer' in request.POST:
            offer_id = request.POST.get('decline_swap_offer')
            offer = SwapOffer.objects.get(pk=offer_id)
            offer.decline_offer()
            return HttpResponse(status=204)
    if request.method == 'DELETE':
            swap_request_instance.delete()
            context = {'DoneDelete': True}
    else:
        # Get user display names from Participation model
        user_display_names = Participation.objects.filter(
            server=swap_request_instance.chore.server
        ).values_list('user__id', 'display_name')

        context = {
            "swap_request_instance": swap_request_instance,
            "swap_request_offers": swap_request_offers,
            "user_display_names": dict(user_display_names)
        }
    
    return render(request, 'servers/partials/manage-swap-request.html', context)

def swap_offer(request, task_id):
    task = get_object_or_404(Chore, pk=task_id)
    swap_requests = SwapRequest.objects.filter(chore=task, status='PENDING')

    # Creating a list of tuples to hold forms for each swap request
    swap_request_forms = [(swap_request, SwapOfferForm(user=request.user, swap_request=swap_request)) for swap_request in swap_requests]

    context = {
        'swap_requests': swap_requests,
        'swap_request_forms': swap_request_forms,
    }
    print(swap_request_forms)
    return render(request, 'servers/partials/swap-offer-form.html', context)


@csrf_exempt
@require_POST
def decline_swap_offer(request, offer_id):
    try:
        offer = SwapOffer.objects.get(pk=offer_id)
        offer.decline_offer()
        return JsonResponse({'status': 'success'}, status=200)
    except SwapOffer.DoesNotExist:
        return JsonResponse({'status': 'not found'}, status=404)   

@csrf_exempt
@require_POST
def accept_swap_offer(request, offer_id):
    offer = SwapOffer.objects.get(pk=offer_id)
    offer.accept_offer()
    return JsonResponse({'status': 'success'}, status=200)



def close_modal(request):
    return HttpResponse('')

def reload_window(request):
    return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})