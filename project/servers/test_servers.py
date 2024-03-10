from django.shortcuts import render
from .models import Server, Participation
from django import http
from django.shortcuts import get_object_or_404
from .models import Participation

# note should have @login_required decorator but its okay for testing
def test_server(request, id):
    
    server = get_object_or_404(Server, id=id)
    if server is None:
        return http.HttpResponseNotFound("server not found")
    
    server_fields = {}
    for field in Server._meta.get_fields():
        field_value = getattr(server, field.name, None)
        server_fields[field.name] = field_value

    # Participation queries are a bit more complicated to do inside template
    # So we'll do it here
    participations = Participation.objects.filter(server=server)
    print(f"Participations in this server {server}: ", 
          [f"{p.display_name} w/ {p.points} points" for p in participations])
    print()

    context = {
        "server": server,
        "server_fields": server_fields,
        "participations": participations
    }
    
    # Example on how to use the super weird but necessary related_name syntax for abstract classes
    # related name = appname_childmodel_related  
    events = server.posts_event_related.all()
    print(f"Events and their time in this server {server}: ", 
          [(e.post_name, (e.date_time.strftime('%A %m/%y %H:%M:%S.%f') or "No time set")) for e in events])
    print()

    return render(request, "servers/test-server.html", context=context)


