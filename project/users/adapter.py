from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# Customize how allauth handles signup from social accounts
# Mainly wanted to hide the email field from user and handle it in the background
# Take rest of the fields from the form and save them here
# https://docs.allauth.org/en/latest/socialaccount/advanced.html
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # Extract the email from the social account's extra data
        social_email = sociallogin.account.extra_data.get('email')
        user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form)
        user.email = social_email
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.phone_number = form.cleaned_data['phone_number']
        user.save()
