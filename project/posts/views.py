from django.shortcuts import render
from .models import Bill, Chore, Event, Comment, Post
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.db.models import Q
from posts.group_page_forms import CommentForm


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
        "description": description,
        "date_created": date_created,
        "cost": cost,
        "split": split,
        "individual_portion": individual_portion,
        "payers": payers,
        "threads": threads,
        "current_user": request.user
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
        "post_name": post_name,
        "description": description,
        "date_created": date_created,
        "due_date": due_date,
        "assigned_to": assigned_to,
        "creator": creator,
        "threads": threads,
        "current_user": request.user
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
        "post_name": post_name,
       "description": description,
       "date_created": date_created,
       "time": time,
       "creator": creator, 
       "threads": threads,
       "current_user": request.user
    })


def add_reply(request, post_type, post_id, parent_comment_id):
    # The parent of the comment chain this reply will belong to
    parent_comment = Comment.objects.get(id=parent_comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.parent_comment = parent_comment
            form.save(commit=True)
        else:
            raise Http404("Form is not valid")
    else:
        initial_data = {
            # The creator of the new reply.
            "author": request.user,
            "parent_comment": parent_comment,
        }
        # Check what type of post this comment will be on and then retrieve it.
        # Store the post as a foreign key in the initial data (links the comment to the post)
        if post_type == "bill":
            initial_data["bill"] = Bill.objects.get(id=post_id)
        elif post_type == "chore":
            initial_data["task"] = Chore.objects.get(id=post_id)
        elif post_type == "event":
            initial_data["event"] = Event.objects.get(id=post_id)
        else:
            raise Http404("Error: " + post_type + " is not a valid post_type")
        
        form = CommentForm(initial=initial_data)

    return render(request, "posts/add-reply.html", {
        "parent_comment": parent_comment,
        "form": form,
        "post_type": post_type,
        "post_id": post_id,
        "parent_comment_id": parent_comment_id,
    })

def add_comment(request, post_type, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
        else:
            raise Http404("Form is not valid")
    else:
        initial_data = {
            # The creator of the comment.
            "author": request.user,
        }
        # Check what type of post this comment will be on and then retrieve it.
        # Store the post as a foreign key in the initial data (links the comment to the post)
        if post_type == "bill":
            initial_data["bill"] = Bill.objects.get(id=post_id)
        elif post_type == "chore":
            initial_data["task"] = Chore.objects.get(id=post_id)
        elif post_type == "event":
            initial_data["event"] = Event.objects.get(id=post_id)
        else:
            raise Http404("Error: " + post_type + " is not a valid post_type")
        
        form = CommentForm(initial=initial_data)

    return render(request, "posts/add-comment.html", {
        "form": form,
        "post_type": post_type,
        "post_id": post_id,
    })