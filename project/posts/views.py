from django.shortcuts import render
from .models import Bill, Chore, Event, Comment

# Create your views here.
def bill(request, id):

    bill = Bill.objects.get(id=id)
    
    creator = bill.creator
    description = bill.description
    date_created = bill.date_created
    cost = bill.cost
    split = "Yes" if bill.split else "No"
    # Check if bill.payers.count is the number of people needing to pay the bill
    individual_portion = cost / bill.payers.count
    payers = bill.payers

    return render(request, "posts/bill.html", {
        "creator": creator
    })
