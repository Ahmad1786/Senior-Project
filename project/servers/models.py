from django.contrib.auth.models import AbstractUser 
from django.db import models
from django.conf import settings
import datetime

class Server():
    group_name = models.CharField(max_length=30)
    group_icon = models.BinaryField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return "Group: " + self.group_name + ", created on " + self.date_created

class Participation():
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    server = models.ForeignKey(Server)
    display_name = models.CharField(max_length=30)
    date_joined = models.DateField(auto_now_add=True)
    points = models.IntegerField(default=0)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return "User: " + self.self.user.name + ", joined " + self.server.group_name + " on " + self.date_joined



