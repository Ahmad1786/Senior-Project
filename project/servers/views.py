from django.shortcuts import render
from posts.models import Bill, Chore, Event
from django.contrib.auth.decorators import login_required

# Create your views here.

# This view will be used to take to the server page
# may be good to also have decorator that checks if the user is a member of the server
@login_required
def server_page(request, server_id):
    # I don't how exactly we want this but for now
    # I will show all the posts of the entire group
    # no other criteria such as show certain dates
    # order by latest post time/date first for now

    # get all the bills for the server
    bills = Bill.objects.filter(server_id=server_id).order_by('-date_created') # latest first
    
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

