from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import User

# The view thats called when a user first logs in
# Show all the fields and their values for the current user
# Meant to be more of a testing page as we are currently working on user model
@login_required
def profile(request):
    user_fields = {} 
    # Iterate over fields, note this includes sensitive fields such as password hash
    for field in User._meta.get_fields():
        field_value = getattr(request.user, field.name, None)
        user_fields[field.name] = field_value
                                            
    return render(request, 'users/profile.html', context={'user_fields': user_fields})

# View to test mail sending: Send mail from backend to requesting user
@login_required
def send_test_mail(request):
    send_mail(
        'Test Email Subject', # email subject
        'Hello, \n\n\nThis is a test email. \n\n\nHave a nice day!', # email body
        None,  # From email - Don't need to specify, just use default 
        [request.user.email], # To email list (Can send to multiple emails at once) 
        fail_silently=False,
    )
    
    return HttpResponse("<h2>Email Sent Successfully!</h2>")

from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
class EditPhoneForm(forms.Form):
    phone_number = PhoneNumberField(required=False, label='New Phone Number',
                                     widget=PhoneNumberPrefixWidget(initial='US', attrs={'placeholder': 'Phone number'}))

is_htmx = lambda request: request.headers.get('HX-Request', False)
# Edit phone number
@login_required
def edit_phone_number(request):
    
    if not is_htmx(request):
        return HttpResponse(status=405)

    if request.method == 'POST':
        form = EditPhoneForm(request.POST)
        if form.is_valid():
            request.user.phone_number = form.cleaned_data['phone_number']
            request.user.save()
            response = HttpResponse(form.cleaned_data['phone_number'])
            response.headers['HX-Retarget'] = '#phone-content'
            return response
        else: 
            response = HttpResponse("Inavlid Phone Number")
            response.headers['HX-Retarget'] = '#dialog'
            return response
    else:
        return render(request, 'users/edit_phone_number.html', context={'form': EditPhoneForm()})
    
def empty_response(request):
    return HttpResponse("")