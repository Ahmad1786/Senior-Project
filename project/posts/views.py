from django.shortcuts import render
from .models import Bill, Chore, Event, Comment

def bill(request, id):

    bill = Bill.objects.get(id=id)
    
    post_name = bill.post_name
    description = bill.description
    date_created = bill.date_created
    cost = bill.cost
    split = "Yes" if bill.split else "No"
    individual_portion = cost / float(bill.payers.count())
    payers = bill.payers
    # Who to pay/ Need to add new field to table and fix later
    #payee = bill.payee

    return render(request, "posts/bill.html", {
        "post_name": post_name,
        "description": description,
        "date_created": date_created,
        "cost": cost,
        "split": split,
        "individual_portion": individual_portion,
        "payers": payers
    })

def chore(request, id):

    chore = Chore.objects.get(id=id)
    
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
    })

def event(request, id):
    
    event = Event.objects.get(id=id)

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
    })

# TODO, complete at some point
def comment(request, id):

    comment = Comment.objects.get(id=id)
