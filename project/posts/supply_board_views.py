from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Bill, Chore, Event, Comment
from servers.models import Server
from django.http import HttpResponse
from django.db.models import F

# These are all the views that will be used for the supply board

# Making seperate file to avoid merge conflicts 
# and keep things separate for now

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
        "server_id": server_id,
    }

    return render(request, "posts/bill-board.html", context=context)


# form to add a bill
from django import forms
class BillForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.current_server_id = kwargs.pop('current_server_id', None)
        server_instance = Server.objects.get(pk=self.current_server_id)
        super(BillForm, self).__init__(*args, **kwargs)
        # initial server value
        self.fields['server'].initial = self.current_server_id
        self.fields['server'].widget = forms.HiddenInput()
        self.fields['creator'].widget = forms.HiddenInput()
        self.fields['creator'].initial = self.request.user
        
        self.fields['payee'].queryset = server_instance.members.all()
  
        self.fields['payee'].initial = self.request.user
        
    def clean(self):
        cleaned_data = super().clean()
        
        # currently allowing for cost of 0 but not empty
        if cleaned_data.get('cost', None) is None:
            self.add_error('cost', 'There must be a cost for the bill')

        if cleaned_data.get('cost', None) is not None and cleaned_data['cost'] < 0:
            self.add_error('cost', 'The cost must be a positive value')
        
        if not cleaned_data['split'] and len(cleaned_data['payee']) > 1:
            self.add_error('payee', 'Can not split bill between multiple people if split is not checked')

        if cleaned_data['split'] and len(cleaned_data['payee']) == 1:
            self.add_error('payee', 'Must split bill between multiple people if split is checked')

        # Decided this may not be what we want but basically i was trying to say
        # if split is false: the user making the post must be the only one paying
        # if not cleaned_data['split']:
        #    print(cleaned_data['payee'])
        #    print(self.request.user)
        #    cleaned_data['payee'] = [self.request.user]
        
        return cleaned_data

    class Meta:
        model = Bill
        fields = ['post_name', 'description', 'cost', 'split','payee', 'server', 'creator']

def add_bill(request, server_id):
    if request.method == 'POST':
        form = BillForm(request.POST, request=request, current_server_id=server_id)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'billListChanged'})
        else:
            return render(request, 'posts/partials/bill-form.html', {
                'form': form,
            })
    
    form = BillForm(request=request, current_server_id=server_id)
    return render(request, 'posts/partials/bill-form.html', {
        'form': form,
    })