from django.shortcuts import render
from posts.models import Bill, Chore, Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from servers.models import Server

# only let user see page if they are in the server
# is_in_server = lambda user, server_id: Server.objects.filter(participations__user=user, id=server_id).exists()
is_in_server = lambda user, server_id: user in Server.objects.get(id=server_id).members.all()

# This view will be used to take to the server page
@login_required
def server_page(request, server_id):

    if not is_in_server(request.user, server_id):
        return HttpResponse(status=403)

    # I don't how exactly we want this but for now
    # I will show all the posts of the entire group
    # no other criteria such as show certain dates
    # order by latest post time/date first for now

    # get all the bills for the server
    bills = Bill.objects.filter(server_id=server_id).order_by('-date_created') # latest first
    for b in bills:
        b.portion = b.individual_portion(request.user)
    
    # note may need to adjust for participation names and other complications
    # just keeping everything simple for now
    
    # now do the same for tasks and events
    tasks = Chore.objects.filter(server_id=server_id).order_by('-date_created')
    events = Event.objects.filter(server_id=server_id).order_by('-date_created')

    context = {
        "bills": bills,
        "tasks": tasks,
        "events": events,
        "server_id": server_id,
    } 
    return render(request, "servers/group-page.html", context=context)

