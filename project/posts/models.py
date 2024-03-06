from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import datetime

class Post(models.model):
    """
    A parent class that Event, Bill, and Chore will extend.
    """
    # Strings
    post_name = models.CharField(max_length = 50)
    description = models.TextField()

class Event():
    


class Bill():
    # Set fields
    posted_date = models.DateField()
    cost = models.FloatField(blank = True)
    split = models.BooleanField(default = True, )
    completed = models.BooleanField(default = False)

class Chore():

class Comment():
    

# extend the User model by extending AbstractUser: see link for details
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    phone_number = PhoneNumberField()

    def save(self, *args, **kwargs):
        # since we are not using username it will just be something hidden to user
        # but superuser will still make own username
        if not self.is_superuser and not self.pk: # save may be called multiple times so do this only on first save
            self.username = self.generate_username()
        super().save(*args, **kwargs)
    
    # String representation of the user object
    # Can also be used as allauth display name
    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"  # "First Last" 
    