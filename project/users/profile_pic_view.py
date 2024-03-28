from django.shortcuts import render
from .models import User
from django.contrib.auth.decorators import login_required
from django import forms


# form to upload a profile picture
class ProfilePicForm(forms.Form):
    profile_pic = forms.ImageField()

# basic page that allows users to upload a profile picture
# and shows their current profile picture or the default one
@login_required
def profile_pic(request):
    
    user = request.user
    picture = user.profile_picture

    # print all fields of picture
    print(picture.__dict__)

    if request.method == "POST":
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            user.profile_picture = form.cleaned_data["profile_pic"]
            user.save()
            context = {
                "form": ProfilePicForm(),
            }
            return render(request, "users/profile-pic.html", context=context)
    
    # else GET request
    context = {
        "form": ProfilePicForm(),
    }
    return render(request, "users/profile-pic.html", context=context)
