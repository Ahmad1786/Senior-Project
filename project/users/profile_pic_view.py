from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

# form to upload a profile picture
#class ProfilePicForm(forms.Form):
#    profile_pic = forms.ImageField()

# use the html form to upload a profile picture
@login_required
@require_POST
def profile_pic(request):
    if request.FILES:
        picture = request.FILES['profile_pic']
        request.user.profile_picture = picture
        request.user.save()
    return redirect('users:profile')