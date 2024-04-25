from django.shortcuts import render
from posts.models import Bill, Chore, Event, SwapRequest, SwapOffer
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from servers.models import Server, Participation, Invitation
from itertools import chain

# only let user see page if they are in the server
# is_in_server = lambda user, server_id: Server.objects.filter(participations__user=user, id=server_id).exists()
is_in_server = lambda user, server_id: user in Server.objects.get(id=server_id).members.all()

# This view will be used to take to the server page
@login_required
def server_page(request, server_id):

    if not is_in_server(request.user, server_id):
        return HttpResponse(status=403)

    # get server participation for request user to ppopulate sidebar
    servers = Server.objects.filter(participations__user=request.user)
    
     # Get the server instance
    server = Server.objects.get(id=server_id)

    # Get the owner's participation
    owner_participation = Participation.objects.filter(server=server, is_owner=True)

    # Get the rest of the participations
    other_participations = Participation.objects.filter(server=server, is_owner=False)

    # Concatenate the two querysets
    participation = owner_participation | other_participations
 
    # get all the bills for the server
    bills = Bill.objects.filter(server_id=server_id).order_by('-date_created') # latest first
    for b in bills:
        b.portion = b.individual_portion(request.user)
    
    # now do the same for tasks and events
    tasks = Chore.objects.filter(server_id=server_id).order_by('-date_created')
    events = Event.objects.filter(server_id=server_id).order_by('-date_created')
    
    # Get all the swap requests and swap offers associated with the server
    swap_requests = SwapRequest.objects.filter(chore__server_id=server_id)
    swap_offers = SwapOffer.objects.filter(offer_chore__server_id=server_id)

    # show server specific display names instead of user's name
    for b in bills:
        b.payers_string = b.payers_string(request.user)
    for t in tasks:
        t.assignee_string = t.assignee_string(request.user)
        t.user_swap_offers = None
    for t in tasks:
        t.swap_requests = SwapRequest.objects.filter(chore=t, status='PENDING').exists()
        swap_request = SwapRequest.objects.filter(chore=t, status='PENDING', requester = request.user).last()
        t.swap_request = swap_request
        t.all_swap_requests = SwapRequest.objects.filter(chore=t, status='PENDING')
        t.user_has_swap_requests = SwapRequest.objects.filter(chore=t, status='PENDING', requester = request.user).exists()
        t.user_has_declined_swap_requests = SwapRequest.objects.filter(chore=t, status='DECLINED', requester = request.user).exists()
        t.user_has_accepted_swap_requests = SwapRequest.objects.filter(chore=t, status='ACCEPTED', requester = request.user).exists()
        if t.swap_requests:
            t.user_swap_offers = SwapOffer.objects.filter(swap_request__in=t.all_swap_requests, user=request.user)
        if t.user_swap_offers is not None:
            t.has_pending_swap_offer = any(offer.status.upper() == 'PENDING' for offer in t.user_swap_offers)
            t.has_accepted_swap_offer = any(offer.status.upper() == 'ACCEPTED' for offer in t.user_swap_offers)
            t.has_all_declined_swap_offer = all(offer.status.upper() == 'DECLINED' for offer in t.user_swap_offers)
    
    for p in chain(bills, tasks, events):
        p.post_creator = p.creator.display_name(Server.objects.get(id=server_id))

    context = {
        "bills": bills,
        "tasks": tasks,
        "events": events,
        "server_id": server_id,
        "servers": servers,
        "participation": participation,
        "swap_requests": swap_requests,
        "swap_offers": swap_offers
    } 
    return render(request, "servers/group-page.html", context=context)

@login_required
def join_server(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        invitation = Invitation.objects.filter(token=token).first()
        if invitation and not invitation.expired:
            server = invitation.server
            user = request.user
            Participation.objects.create(user=user, server=server, is_owner=False)
            invitation.delete()
            return JsonResponse({'message': 'Successfully joined the server.'})
        else:
            return JsonResponse({'error': 'Invalid or expired token.'}, status=400)
    return JsonResponse({'error': 'Invalid request.'}, status=400)

@login_required
def create_server(request):
    if request.method == 'POST':
        server_name = request.POST.get('server_name')
        invite_emails = request.POST.get('invite_emails')
        # Create the server
        server = Server.objects.create(group_name=server_name)
        # Process invite emails (you'll need to implement this logic)
        # For now, just return a success message
        return JsonResponse({'message': 'Server created successfully.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

@require_POST
def create_invitation(request):
    server_id = request.POST.get('server_id')
    invited_email = request.POST.get('invite_email')
    
    # Assuming you have a way to get the server object based on server_id
    server = Server.objects.get(id=server_id)
    
    # Create the invitation
    invitation = Invitation.create_invitation(server, invited_email)
    
    # You can return a success message or any relevant data
    return JsonResponse({'message': 'Invitation created successfully'})