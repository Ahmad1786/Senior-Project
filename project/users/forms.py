from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# Customize the default signup form for normal signups
class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        # Can customize the parent class/form fields here such as email or 
        # setting initial values (assuming not already set if in social signup form)
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email (Required)"
        self.fields['password1'].label = "Password (Required)"

    first_name = forms.CharField(max_length=30, required=True, label="First Name (Required)", 
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True, label="Last Name (Required)", 
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    phone_number = PhoneNumberField(required=False, label='Phone Number',
                                     widget=PhoneNumberPrefixWidget(initial='US', attrs={'placeholder': 'Phone number'}))

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        
        user.save()

        # You must return the original result.
        return user

# Customize the default signup form for social signups
class MyCustomSocialSignupForm(SocialSignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSocialSignupForm, self).__init__(*args, **kwargs)

        # hide the email and don't require it in the form- handle it in the adapter instead
        self.fields['email'].widget = forms.HiddenInput()
        self.fields['email'].required = False
        
    # For the most part First and Last should already be given by the social account provider
    first_name = forms.CharField(max_length=30, required=True, label = "First Name (Required)", 
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True, label = "Last Name (Required)", 
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    phone_number = PhoneNumberField(required=False, label='Phone Number',
                                widget=PhoneNumberPrefixWidget(initial='US', attrs={'placeholder': 'Phone number'}))

    
    # Handle saving the user in the adapter instead of the form
    # Adapter has access to form and request
    # def save(self, request)


