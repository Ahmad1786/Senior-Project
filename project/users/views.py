from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail

User = get_user_model() # gets current user model

# The view thats called when a user first logs in
# Meant to be more of a testing page as we are currently working on user model
@login_required
def profile(request):
    user_fields = {} 
    # Iterate over fields, exclude sensitive fields explicitly
    for field in User._meta.get_fields():
        field_value = getattr(request.user, field.name, None)
        user_fields[field.name] = field_value
                                            
    return render(request, 'users/profile.html', context={'user_fields': user_fields})

# View to test mail sending: Send mail from backend to requesting user
@login_required
def send_test_mail(request):
    send_mail(
        'Test Email Subject', # email subject
        'This is nothing more than a test email ..... \n\n\nHave a nice day!', # email body
        None,  # From email - Don't need to specify, just use default 
        [request.user.email], # To email list (Can send to multiple emails) 
        fail_silently=False,
    )
    
    return HttpResponse("<h2>Email Sent Successfully!</h2>")