from django.shortcuts import render
from .models import User
from django.shortcuts import get_object_or_404

# test view that will show all things related to the user
# note should have @login_required decorator but its okay for testing
def test_user(request, id):
    # query by user by id
    
    user = get_object_or_404(User, id=id)

    # get participations
    participations = user.participations.all()

    user_fields = {} 
    # Iterate over fields, note this includes sensitive fields such as password hash
    for field in User._meta.get_fields():
        field_value = getattr(user, field.name, None)
        user_fields[field.name] = field_value

    owned_servers = user.servers.filter(participations__is_owner=True)
    owned_servers_ids = [server.id for server in owned_servers]

    context = {
        "user": user,
        "participations": participations,
        "user_fields": user_fields,
        "owned_servers_ids": owned_servers_ids
    }

    return render(request, "users/test-user.html", context=context)
