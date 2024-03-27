from django.shortcuts import render
from .models import User
from django.contrib.auth.decorators import login_required
from django import forms


# form to upload a profile picture
class ProfilePicForm(forms.Form):
    profile_pic = forms.ImageField()


@login_required
def profile_pic(request):
    
    user = request.user
    picture = user.profile_picture

    # print all fields of picture
    print(picture.__dict__)

    context = {
        "form": ProfilePicForm(),
    }

    return render(request, "users/profile-pic.html", context=context)
