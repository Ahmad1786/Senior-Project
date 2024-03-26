from django.shortcuts import render
from posts.models import Bill, Chore, Event
from django.contrib.auth.decorators import login_required
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

    # get all the bills for the server
    bills = Bill.objects.filter(server_id=server_id).order_by('-date_created') # latest first
    for b in bills:
        b.portion = b.individual_portion(request.user)
    
    # now do the same for tasks and events
    tasks = Chore.objects.filter(server_id=server_id).order_by('-date_created')
    events = Event.objects.filter(server_id=server_id).order_by('-date_created')

    # show server specific display names instead of user's name
    for b in bills:
        b.payers_string = b.payers_string(request.user)
    for t in tasks:
        t.assignee_string = t.assignee_string(request.user)

    for p in chain(bills, tasks, events):
        p.post_creator = p.creator.display_name(Server.objects.get(id=server_id))

    context = {
        "bills": bills,
        "tasks": tasks,
        "events": events,
        "server_id": server_id,
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
