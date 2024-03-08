from django.shortcuts import render
from .models import User
from django import http
from django.shortcuts import get_object_or_404

# test view that will show all things related to the user
# note should have @login_required decorator but its okay for testing
def test_user(request, id):
    # query by user by id
    
    user = get_object_or_404(User, id=id)
    if user is None:
        return http.HttpResponseNotFound("User not found")
    
    # get participations
    participations = user.participations.all()

    user_fields = {} 
    # Iterate over fields, note this includes sensitive fields such as password hash
    for field in User._meta.get_fields():
        field_value = getattr(user, field.name, None)
        user_fields[field.name] = field_value

    context = {
        "user": user,
        "participations": participations,
        "user_fields": user_fields
    }

    return render(request, "users/test-user.html", context=context)
