from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Bill, Chore, Event, Comment
from django.http import HttpResponse
from django.db.models import F

# These are all the views that will be used for the supply board

# Making seperate file to avoid merge conflicts 
# and keep things separate for now

# This is a helper function to get name of person who created bill
def get_person(current_user_id, creator_id):
    if (current_user_id == creator_id):
        return "You"
    return "Someone else"

@login_required
def supply_board(request, server_id):
    
    # I don't how exactly we want this but for now
    # I will show all the bills of the entire group
    # no other criteria such as show certain dates
    # order by latest date first for now

    # get all the bills for the server
    bills = Bill.objects.filter(server_id=server_id).order_by('-date_created') # latest first
    


    # note may need to adjust for participation names and other complications
    # just keeping everything simple for now
    

    context = {
        "bills": bills,
    }

    return render(request, "posts/bill-board.html", context=context)

# form to add a bill
from django import forms
class BillForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.current_server_id = kwargs.pop('current_server_id', None)
        super(BillForm, self).__init__(*args, **kwargs)
        # initial server value
        self.fields['server'].initial = self.current_server_id
        self.fields['creator'].initial = self.request.user.id 
        

    class Meta:
        model = Bill
        fields = ['post_name', 'description', 'cost', 'split', 'server', 'creator']

def add_bill(request, server_id):
    if request.method == 'POST':
        form = BillForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'billListChanged'})
    
    form = BillForm(request=request, current_server_id=server_id)
    return render(request, 'posts/partials/bill-form.html', {
        'form': form,
    })