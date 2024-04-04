from django.shortcuts import render
from posts.models import Bill, Chore, Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from servers.models import Server, Participation

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

    # show server specific display names instead of user's name
    for b in bills:
        b.payers_string = b.payers_string(request.user)
    for t in tasks:
        t.assignee_string = t.assignee_string(request.user)



    context = {
        "bills": bills,
        "tasks": tasks,
        "events": events,
        "server_id": server_id,
        "servers": servers,
        "participation": participation,
    } 
    return render(request, "servers/group-page2.html", context=context)
