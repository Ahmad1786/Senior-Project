from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db import models
from serverparticipation.models import Server

class Post(models.Model):
    """
    A parent class that Event, Bill, and Chore will extend.
    """
    # Foreign keys
    server = models.ForeignKey(Server)

    # Field attributes
    post_name = models.CharField(max_length = 50)
    description = models.TextField()

    def __str__(self):
        return "Server: " + self.server + ", post_name: " + self.post_name + ", description: " + self.description

# Extends Post
class Event(Post):
    # Field attributes
    creator = models.CharField(max_length = 30)
    date_time = models.DateTimeField()

    def __str__(self):
        return self.creator + " created an event " + Post.post_name + " (" + Post.description + ") that takes place at " + self.date_time

# Extends Post
class Bill(Post):
    # Foreign keys
    payee = models.ManyToManyField(settings.AUTH_USER_MODEL)
    bill_creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Field attributes
    posted_date = models.DateField()
    cost = models.FloatField(blank = True, null = True)
    split = models.BooleanField(default = True)
    completed = models.BooleanField(default = False)

    def __str__(self):
        return self.bill_creator + " created a bill " + Post.post_name + " (" + Post.description + ") for " + self.cost + " due by " + self.due_date

# Extends Post
class Chore(Post):
    # Foreign keys
    assignee = models.ManyToManyField(settings.AUTH_USER_MODEL)

    # Field attributes
    due_date = models.DateField()
    assigned_date = models.DateField()
    completed = models.BooleanField(default = False)
    point_value = models.IntegerField(default = 0)

    def __str__(self):
        return self.assignee.name + " is assigned to " + Post.post_name + " (" + Post.description + ") due by " + self.due_date

class Comment(models.Model):
    # Foreign keys
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    task = models.ForeignKey(Chore, null = True)
    event = models.ForeignKey(Event, null = True)
    bill = models.ForeignKey(Bill, null = True)
    parent_comment = models.ForeignKey("self", null = True, related_name = "replies")

    # Field attributes
    content = models.TextField()
    date_time = models.DateTimeField()

    def __str__(self):
        return self.user + " (" + self.date_time +")" + "commented \"" + self.content + "\""
    
