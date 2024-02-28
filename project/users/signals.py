# Was trying to find a way to capitalize social users name before they are logged in. 
# (Sometimes google returned the name in lowercase)
# Allauth emits a signal called pre_social_login which we can use to update the user's
# information before they are logged in (and by extension before they are brought to signup after google connection)
# silly example and also could have done this in adapter as well but good way to learn about signals

from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

# https://docs.allauth.org/en/latest/socialaccount/signals.html
@receiver(pre_social_login)
def update_social_user_info(request, sociallogin, **kwargs):
    """
    Signal handler to update information of a social user before login.
    """
    first_name = sociallogin.account.extra_data.get('given_name')
    last_name = sociallogin.account.extra_data.get('family_name')

    if first_name:
        sociallogin.user.first_name = first_name.capitalize()
    if last_name:   
        sociallogin.user.last_name = last_name.capitalize()
    
    # can save the model here but will do it in the form or adapter instead



    
