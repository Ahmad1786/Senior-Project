from django.shortcuts import redirect, render
from .models import Bill, Chore, Event, Comment, PostImage
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.db.models import Q
from posts.group_page_forms import CommentForm
from django.views.decorators.http import require_POST
from django.utils import timezone


@login_required
def bill(request, id):
    bill = Bill.objects.get(id=id)
    threads = {}
    # Get parent comments that belong to this event
    parent_comments =  Comment.objects.filter(Q(bill_id=bill.id) & Q(parent_comment=None))
    for comment in parent_comments:
        # Append the dictionary so that the key is a parent and the value contains the replies
        threads[comment] = Comment.objects.filter(parent_comment=comment)

    post_id = id
    post_name = bill.post_name
    description = bill.description
    date_created = bill.date_created
    cost = bill.cost
    split = "Yes" if bill.split else "No"
    individual_portion = bill.individual_portion(request.user)
    payers = bill.payers
    # Who to pay/ Need to add new field to table and fix later
    #payee = bill.payee

    return render(request, "posts/bill.html", {
        "post_id": post_id,
        "post_name": post_name,
        "post_type": "bill",
        "description": description,
        "date_created": date_created,
        "cost": cost,
        "split": split,
        "individual_portion": individual_portion,
        "payers": payers,
    })

@login_required
def chore(request, id):
    chore = Chore.objects.get(id=id)
    threads = {}
    # Get parent comments that belong to this event
    parent_comments =  Comment.objects.filter(Q(task_id=chore.id) & Q(parent_comment=None))
    for comment in parent_comments:
        # Append the dictionary so that the key is a parent and the value contains the replies
        threads[comment] = Comment.objects.filter(parent_comment=comment)

    post_name = chore.post_name
    description = chore.description
    date_created = chore.date_created
    due_date = chore.due_date
    assignees = chore.assignee.all()
    # Fix formatting at some point
    assigned_to = [assignee.first_name for assignee in assignees]
    creator = chore.creator

    return render(request, "posts/chore.html", {
        "post_id": id,
        "post_name": post_name,
        "description": description,
        "post_type": "chore",
        "date_created": date_created,
        "due_date": due_date,
        "assigned_to": assigned_to,
        "creator": creator,
        "chore_images": chore.images.all(),
        "is_assigned": request.user in chore.assignee.all(),
    })

@login_required
def event(request, id):
    event = Event.objects.get(id=id)
    threads = {}
    # Get parent comments that belong to this event
    parent_comments =  Comment.objects.filter(Q(event_id=event.id) & Q(parent_comment=None))
    for comment in parent_comments:
        # Append the dictionary so that the key is a parent and the value contains the replies
        threads[comment] = Comment.objects.filter(parent_comment=comment)

    post_name = event.post_name
    description = event.description
    date_created = event.date_created
    time = event.date_time
    creator = event.creator
    
    return render(request, "posts/event.html", {
       "post_id": id, 
       "post_name": post_name,
       "post_type": "event",
       "description": description,
       "date_created": date_created,
       "time": time,
       "creator": creator, 
    })

# use the html form to upload a picture to post
@login_required
@require_POST
def chore_pic(request, post_id):
    if request.FILES:
        picture = request.FILES['chore_pic']
        
        post = Chore.objects.get(id=post_id)
        post_image = PostImage(image=picture, date_uploaded=timezone.now(), post=post)
        post_image.save()

    return redirect('posts:chore', post_id)