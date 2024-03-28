from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# extend the User model by extending AbstractUser: see link for details
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, default='profile_pics/default_profile.png', upload_to='profile_pics')

    def save(self, *args, **kwargs):
        # since we are not using username it will just be something hidden to user
        # but superuser will still make own username
        if not self.is_superuser and not self.pk: # save may be called multiple times so do this only on first save
            self.username = self.generate_username()
        super().save(*args, **kwargs)
    
    # Username will be strictly for internal puposes - hidden from user
    # Generate a unique username automatically on signup
    def generate_username(self):
        base_username = self.first_name.capitalize() + self.last_name.capitalize()
        return base_username + str(User.objects.filter(username__startswith=base_username).count() + 1)
    
    # String representation of the user object
    # Can also be used as allauth display name
    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"  # "First Last" 
    
    def display_name(self, server):
        participation = self.participations.get(server=server)
        return participation.display_name

# Done by Luke
# Should wait until we have a better understanding of the project to implement this - Muhammad
# Model for Notification
# class Notification():
       # user = models.ForeignKey(User, on_delete=models.CASCADE) - This should probably be a MtoM though - Muhammad
       # message = models.TextField()
       # created = models.DateTimeField(default=timezone.now)
    
