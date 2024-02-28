from django.db import models
from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField

# extend the User model by extending AbstractUser: see link for details
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# Just setting up basic structure - implement later
class User(AbstractUser):
    phone_number = PhoneNumberField()

    def save(self, *args, **kwargs):
        # since we are not using username it will just be something hidden in the background
        # but superuser will still make own username
        if not self.is_superuser and not self.pk: # also have to check if record already exists because save gets called multiple times
            self.username = self.generate_username()
        super().save(*args, **kwargs)
    
    # Username will be strictly for internal puposes - mostly hidden from user
    # Still need to ensure it is unique
    def generate_username(self):
        base_username = self.first_name.capitalize() + self.last_name.capitalize()
        return base_username + str(User.objects.filter(username__startswith=base_username).count() + 1)
    
    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"  # "First Last" 
