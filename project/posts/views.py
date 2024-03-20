from django.shortcuts import render
from .models import Bill, Chore, Event, Comment

def bill(request, id):

    bill = Bill.objects.get(id=id)
    
    creator = bill.creator
    description = bill.description
    date_created = bill.date_created
    cost = bill.cost
    split = "Yes" if bill.split else "No"
    individual_portion = cost / float(bill.payers.count())
    payers = bill.payers
    # Who to pay/ Need to add new field to table and fix later
    #payee = bill.payee

    return render(request, "posts/bill.html", {
        "bill": bill,
        "creator": creator,
        "description": description,
        "date_created": date_created,
        "cost": cost,
        "split": split,
        "individual_portion": individual_portion
    })
