from django.conf import settings
from django.db import models
from servers.models import Server

class Post(models.Model):
    """
    An Abstract parent class that Event, Bill, and Chore will extend.
    """
    # Foreign keys
    # related_name = "posts" but need to tune for abstract classes
    server = models.ForeignKey(Server, on_delete = models.CASCADE, 
                               related_name = "%(app_label)s_%(class)s_posts") 
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, 
                                related_name = "%(app_label)s_%(class)s_posts") 

    # Field attributes
    post_name = models.CharField(max_length = 50)
    description = models.TextField()
    date_created = models.DateField(auto_now_add = True)

    # make into Abstract class - won't be creating Post objects
    class Meta:
        abstract = True

    def __str__(self):
        return "Server: " + self.server + ", post_name: " + self.post_name + ", description: " + self.description

# Extends Post
class Event(Post):
    # Field attributes
    # creator = models.CharField(max_length = 30) # bad practice - may cause problems later
    date_time = models.DateTimeField(null = True, blank = True) # date and time of the event (not the date it was created)

    def __str__(self):
        return self.creator + " created an event " + Post.post_name + " (" + Post.description + ") that takes place at " + self.date_time

# Extends Post
class Bill(Post):
    # Foreign keys
    # payee = people who receive the bill vs payer = people who pay the bill
    # Can have multiple people who pay the money
    payee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bills")
    # bill_creator = models.ForeignKey(settings.AUTH_USER_MODEL) - relationship already established in Post - just use property decorator

    # Field attributes
    # posted_date = models.DateField()
    cost = models.FloatField(blank = True, null = True)
    split = models.BooleanField(default = True)
    completed = models.BooleanField(default = False)

    @property
    def bill_creator(self):
        return self.creator
    
    @property
    def posted_date(self):
        return self.date_created

    def __str__(self):
        return self.bill_creator + " created a bill " + Post.post_name + " (" + Post.description + ") for " + self.cost + " due by " + self.posted_date

# Extends Post
class Chore(Post):
    # Foreign keys
    # assignee = the person who is assigned the chore/can have multiple people working on the chore
    assignee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_chores")

    # Field attributes
    due_date = models.DateField()
    # make assigned date the current date it was created
    # assigned_date = models.DateField(auto_now_add = True) - since both chore and bill have a date_created => move to parent model
    completed = models.BooleanField(default = False)
    point_value = models.IntegerField(default = 0)

    @property
    def assigner(self):
        return self.creator # Assume person who creates the chore is the assigner?
    
    @property
    def assigned_date(self):
        return self.date_created

    def __str__(self):
        return self.assignee.name + " is assigned to " + Post.post_name + " (" + Post.description + ") due by " + self.due_date

class Comment(models.Model):
    # Foreign keys
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "comments")
    task = models.ForeignKey(Chore, on_delete = models.CASCADE, null = True, related_name = "comments")
    event = models.ForeignKey(Event, on_delete = models.CASCADE, null = True, related_name = "comments")
    bill = models.ForeignKey(Bill, on_delete = models.CASCADE, null = True, related_name = "comments")
    parent_comment = models.ForeignKey("self", null = True, on_delete = models.CASCADE , related_name = "replies")

    # Field attributes
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user + " (" + self.date_time +")" + "commented \"" + self.content + "\""
    
