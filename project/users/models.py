from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# extend the User model by extending AbstractUser: see link for details
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# Just setting up basic structure - implement later
class User(AbstractUser):
    # no additions for now (add custom fields later)
    pass
