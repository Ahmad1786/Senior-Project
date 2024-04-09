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

from django.db.models.signals import post_save
from posts.models import Chore
from users.models import Notification
from django.contrib.contenttypes.models import ContentType

# does not work for m2m fields
#@receiver(post_save, sender=Chore)
#def create_task_notification(sender, instance, created, **kwargs):
#    """
#    Signal handler to create a notification when a task is created.
#    """
#    if created:
#        Notification.objects.create(
#            message=f"Task '{instance.post_name}' has been assigned to you",
#            content_type=ContentType.objects.get_for_model(Chore),
#            object_id=instance.id,
#        )
            
# instead use m2m_changed signal
from django.db.models.signals import m2m_changed
@receiver(m2m_changed, sender=Chore.assignee.through)
def create_task_notification(sender, instance, action, **kwargs):
    """
    Signal handler to create a notification when a task is assigned to a user.
    """
    if action == "post_add":
        n = Notification.objects.create(
                message=f"Task {instance.post_name} in {instance.server} has been assigned to you",
                content_type=ContentType.objects.get_for_model(Chore),
                object_id=instance.id,
            )
        
        n.receivers.set(instance.assignee.all())
        n.save()

from posts.models import Bill
@receiver(m2m_changed, sender=Bill.payers.through)
def create_bill_notification(sender, instance, action, **kwargs):
    """
    Signal handler to create a notification when a bill is assigned to a user.
    """
    if action == "post_add":
        n = Notification.objects.create(
                message=f"You have been added as a payer to Bill {instance.post_name} in {instance.server}",
                content_type=ContentType.objects.get_for_model(Bill),
                object_id=instance.id,
            )
        
        n.receivers.set(instance.payers.all())
        n.save()

from posts.models import Event
@receiver(post_save, sender=Event)
def create_event_notification(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a Event is created.
    """
    if created:
        n = Notification.objects.create(
            message=f"There is a new event in {instance.server.group_name}: {instance.post_name} on {instance.date_time}",
            content_type=ContentType.objects.get_for_model(Event),
            object_id=instance.id,
        )
        n.receivers.set(instance.server.members.all())
        n.save()