from django.conf import settings
from django.db import models
from servers.models import Server
from posts.models import *
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
import datetime

class Post(models.Model):
    """
    An Abstract parent class that Event, Bill, and Chore will extend.
    """
    # Foreign keys
    # related_name = "posts" but need to tune for abstract classes
    server = models.ForeignKey(Server, on_delete = models.CASCADE, 
                               related_name = "%(app_label)s_%(class)s_related") 
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, 
                                related_name = "%(app_label)s_%(class)s_related") 

    # Field attributes
    post_name = models.CharField(max_length = 50)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add = True)

    class Meta:
        abstract = True

# Extends Post
class Event(Post):
    date_time = models.DateTimeField(null = True, blank = True) # date and time of the event (not the date it was created)

    def __str__(self):
        return f"Event: {self.post_name} in {self.server.group_name} on {self.date_time.strftime('%m/%d/%Y %I:%M %p')}"

# Extends Post
class Bill(Post):
    # Foreign keys
    # payees = people who receive the bill vs payers = people who pay the bill
    payers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bills")
    # bill_creator = models.ForeignKey(settings.AUTH_USER_MODEL) - relationship already established in Post - just use property decorator

    # Field attributes
    cost = models.DecimalField(blank = True, null = True, max_digits = 10, decimal_places = 2)
    split = models.BooleanField(default = True)
    completed = models.BooleanField(default = False)

    @property
    def bill_creator(self):
        return self.creator
    
    @property
    def posted_date(self):
        return self.date_created
    
    def individual_portion(self, user):
        if user in self.payers.all():
            # ensure no more than 2 decimal places result
            return (self.cost / Decimal(len(self.payers.all()))).quantize(Decimal('0.01'), rounding = ROUND_HALF_UP)
        return Decimal('0.00')
    
    def payers_string(self, user):
        if len(self.payers.all()) == 1:
            return "You" if user in self.payers.all() else self.payers.first().display_name(self.server)
        if user in self.payers.all():
            return f"You, {', '.join([p.display_name(self.server) for p in self.payers.all() if p != user])}"
        return ', '.join([p.display_name(self.server) for p in self.payers.all()]) 

    def __str__(self):
        return f"Bill: {self.post_name} in {self.server.group_name} (${self.cost})"

class Chore(Post):
    # Foreign keys
    # assignee = the people assigned with chore
    assignee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_chores", blank=True)

    # Field attributes
    due_date = models.DateField()
    # make assigned date the current date it was created ?
    completed = models.BooleanField(default = False)
    point_value = models.IntegerField(default = 0)

    @property
    def assigner(self):
        return self.creator # Assume person who creates the chore is the assigner?
    
    @property
    def assigned_date(self):
        return self.date_created
    
    def assignee_string(self, user):
        if len(self.assignee.all()) == 1:
            return "You" if user in self.assignee.all() else self.assignee.first().display_name(self.server)
        if user in self.assignee.all():
            return f"You, {', '.join([a.display_name(self.server) for a in self.assignee.all() if a != user])}"
        return ', '.join([a.display_name(self.server) for a in self.assignee.all()]) 

    @property
    def point_val(self):

        if self.completed:
            return 10
        else:
            # Calculate points based on due date
            days_remaining = (self.due_date - datetime.now().date()).days
            if days_remaining < 1:
                # Point system based on how early a task is completed?
                return 0
            elif days_remaining <= 3:
                return 8
            elif days_remaining <= 7:
                return 5
            else:
                return 3


    def __str__(self):
        return f"Chore: {self.post_name} in {self.server.group_name}"

class Comment(models.Model):
    # Foreign keys
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "comments")
    task = models.ForeignKey(Chore, on_delete = models.CASCADE, null = True, blank = True, related_name = "comments")
    event = models.ForeignKey(Event, on_delete = models.CASCADE, null = True, blank = True, related_name = "comments")
    bill = models.ForeignKey(Bill, on_delete = models.CASCADE, null = True, blank = True, related_name = "comments")
    parent_comment = models.ForeignKey("self", null = True, blank = True, on_delete = models.CASCADE , related_name = "replies")

    # Field attributes
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        post = self.task or self.event or self.bill
        return f"Comment by {self.author} in {post.post_name}"


class SwapRequest(models.Model):
    chore = models.ForeignKey("Chore", on_delete=models.CASCADE, related_name="swap_chore")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="swap_requests")
    status_choices = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Swap request by {self.requester} for {self.chore}"

    def set_status(self):
        total_users = self.chore.server.members.count()
        declined_offers = SwapOffer.objects.filter(swap_request=self, status='DECLINED').count()

        if declined_offers == total_users - self.chore.assignee.count():
            self.status = 'DECLINED'
        elif self.status != 'ACCEPTED':
            self.status = 'PENDING'
        self.save()

    def accept_offer(self):
        if self.status == 'PENDING':
            self.status = 'ACCEPTED'
            self.save()
        else:
            raise ValueError("Cannot accept offer for a swap request that is not pending.")

    @classmethod
    def create_swap_request(cls, chore, requester):
        return cls.objects.create(chore=chore, requester=requester, status='PENDING', date_requested=timezone.now())

    def delete_request(self):
        self.delete()
        
class SwapOffer(models.Model):
    swap_request = models.ForeignKey(SwapRequest, on_delete=models.CASCADE, related_name='swap_offers')
    offer_chore = models.ForeignKey(Chore, on_delete=models.CASCADE, null=True, blank=True, related_name='swap_offers_related')  # Change related_name value
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_choices = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.swap_request.set_status()
    
    def accept_offer(self):
        if self.status == 'PENDING' and self.swap_request.status == 'PENDING':
            if self.offer_chore:
                
                #Add Swap offer user to assignees for chore they are swapping with
                self.offer_chore.assignee.add(self.swap_request.requester)
                #Remove user who made swap offer from the chore they are trying to swap out of
                self.offer_chore.assignee.remove(self.user)
                
                #Add swap request user to assignees of chore they are swapping into
                self.swap_request.chore.assignee.add(self.user)
                #Remove swap request user from chore they are swapping out of
                self.swap_request.chore.assignee.remove(self.swap_request.requester)

                self.status = 'ACCEPTED'
                self.save()
                self.swap_request.accept_offer()
            else:
                # Automatically accept the offer with no chore in return
                self.swap_request.chore.assignee.remove(self.swap_request.requester)
                self.swap_request.chore.assignee.add(self.user)
                self.status = 'ACCEPTED'
                self.save()
                self.swap_request.accept_offer()
        else:
            raise ValueError("Cannot accept offer that is not pending.")

    def decline_offer(self):
        if self.status == 'PENDING':
            self.status = 'DECLINED'
            self.save()
            self.swap_request.set_status()
        else:
            raise ValueError("Cannot decline offer that is not pending.")
        
    @classmethod
    def create_offer(cls, swap_request, offer_chore, status, user):
        if isinstance(swap_request, SwapRequest) and swap_request.status == 'PENDING':
            if offer_chore is not None:
                offer = cls(swap_request=swap_request, status = status, offer_chore=offer_chore, user=user)
                offer.save()
                swap_request.set_status()
                return offer
            elif offer_chore is None:
                offer = cls(swap_request=swap_request, user=user)
                offer.save()
                swap_request.accept_offer()
                return offer
        else:
            raise ValueError("Cannot create offer for a swap request that is not pending.")
    
    def delete_offer(self):
        self.delete()
        self.swap_request.set_status()
    
    def update_offer(self, offer_chore=None):
        if self.status == 'PENDING' and self.swap_request.status == 'PENDING':
            if offer_chore:
                self.offer_chore = offer_chore
                self.save()
            elif offer_chore:
                self.swap_request.accept_offer()
                self.save()
        else:
            raise ValueError("Cannot update offer that is not pending.")

        

from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import get_current_timezone 

class RecurringTask(models.Model):

    server = models.ForeignKey(Server, on_delete = models.CASCADE, related_name = "recurring_tasks")
    assignee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_recurring_tasks", blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "created_recurring_tasks")

    # (null=True, blank=True) for testing purposes
    title = models.CharField(max_length = 50)
    description = models.TextField(null=True, blank=True)
    first_due_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    point_value = models.IntegerField(default = 0)

    FREQUENCY_CHOICES = [
        ('minute', 'Minute'), # for testing purposes
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
    ]
    
    recurring_period = models.IntegerField(null=True, blank=True) # how often
    recurring_unit = models.CharField(max_length = 10, choices = FREQUENCY_CHOICES) # unit of repetition

    assignee_index = models.IntegerField(default=0)

    def __str__(self):
        return f"Recurring Task: {self.title} in {self.server.group_name}"
    
    def get_next_assignee(self):
        assignees = list(self.assignee.all())
        if not assignees:
            return None
        # Calculate the correct index and access the assignee
        next_assignee_index = self.assignee_index % len(assignees)
        next_assignee = assignees[next_assignee_index]
        
        # Increment the assignee_index for next time
        self.assignee_index = (self.assignee_index + 1) % len(assignees)
        self.save()
        return next_assignee
    
    def get_next_due_date(self):
        if not self.due_date:
            return self.first_due_date
        if self.recurring_unit == 'minute':
            return self.due_date + timedelta(minutes=self.recurring_period)
        elif self.recurring_unit == 'day':
            return self.due_date + timedelta(days=self.recurring_period)
        elif self.recurring_unit == 'week':
            return self.due_date + timedelta(weeks=self.recurring_period)
        elif self.recurring_unit == 'month':
            return self.due_date + timedelta(days=30*self.recurring_period)

    def check_and_create_chore(self):
        now = timezone.now().astimezone(get_current_timezone())
        if not self.due_date or now >= self.due_date:
            next_assignee = self.get_next_assignee()
            next_due_date = self.get_next_due_date()
            self.due_date = next_due_date  # Update the due date for the next iteration
            self.save()
            
            chore = Chore.objects.create(
                server=self.server,
                creator=self.creator,
                post_name=self.title,
                description=self.description,
                due_date=next_due_date.date(),
                point_value=self.point_value,
            )
            chore.assignee.add(next_assignee)
            
        return None

