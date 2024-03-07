from django.contrib.auth.models import AbstractUser 
from django.db import models
import datetime
# Create your models here.

class Server(models.Model):
    group_name = models.CharField(max_length=100)
    group_icon = models.BinaryField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.group_name

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    points = models.IntegerField(default=0)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name | self.server.group_name



