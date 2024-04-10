from django.conf import settings
from django.db import models
from servers.models import Server
from decimal import Decimal, ROUND_HALF_UP

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
    # Foreign keys
    chore = models.ForeignKey("Chore", on_delete=models.CASCADE, related_name="swap_requests")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="swap_requests")
    offer = models.ForeignKey("Chore", on_delete=models.CASCADE, null=True, blank=True, related_name="swap_offers")
    status_choices = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Swap request by {self.requester} for {self.chore}"

    def accept_offer(self, offer_chore):
        if self.status == 'PENDING':
            self.status = 'ACCEPTED'
            self.offer = offer_chore
            self.save()
        else:
            raise ValueError("Cannot accept offer for a swap request that is not pending.")

    def decline_offer(self):
        if self.status == 'PENDING':
            self.status = 'DECLINED'
            self.save()
        else:
            raise ValueError("Cannot decline offer for a swap request that is not pending.")
        
class SwapOffer(models.Model):
    swap_request = models.ForeignKey(SwapRequest, on_delete=models.CASCADE, related_name='swap_offers')
    offer_chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name='swap_offers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_choices = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def accept_offer(self):
        if self.status == 'PENDING':
            if self.offer_chore:
                # Replace the specific assignee of offer_chore with the requester of swap_request
                offer_chore_assignees = self.offer_chore.assignee.all()
                offer_chore_assignees = [self.swap_request.requester if assignee == self.user else assignee for assignee in offer_chore_assignees if assignee != self.user]
                self.offer_chore.assignee.set(offer_chore_assignees)

                # Replace the specific assignee of swap_request.chore with the user associated with the swap offer
                swap_request_chore_assignees = self.swap_request.chore.assignee.all()
                swap_request_chore_assignees = [self.user if assignee == self.swap_request.requester else assignee for assignee in swap_request_chore_assignees]
                self.swap_request.chore.assignee.set(swap_request_chore_assignees)

                self.status = 'ACCEPTED'
                self.save()
                self.swap_request.accept_offer(self.offer_chore)
            else:
                # Automatically accept the offer with no chore in return
                self.swap_request.chore.assignee.remove(self.swap_request.requester)
                self.swap_request.chore.assignee.add(self.user)
                self.status = 'ACCEPTED'
                self.save()
                self.swap_request.accept_offer(self.offer_chore)
        else:
            raise ValueError("Cannot accept offer that is not pending.")

    def decline_offer(self):
        if self.status == 'PENDING':
            self.status = 'DECLINED'
            self.save()
        else:
            raise ValueError("Cannot decline offer that is not pending.")