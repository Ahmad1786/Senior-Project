# THESE ARE THE INITIAL FORMS FOR THE SERVERS APP
# THESE WILL BE USED TO MAKE THE 3 MAIN POSTS IN THE GROUP PAGE

from django import forms
from posts.models import Bill, Event, Chore
from servers.models import Server

# NOTE: MADE these forms kind of fast, so they may not be the 
# best/most efficient way to do things, but good enough for now

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





class TaskForm(forms.ModelForm):
    pass
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.current_server_id = kwargs.pop('current_server_id', None)
        server_instance = Server.objects.get(pk=self.current_server_id)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        # initial server value
        self.fields['server'].initial = self.current_server_id
        self.fields['server'].widget = forms.HiddenInput()
        self.fields['creator'].widget = forms.HiddenInput()
        self.fields['creator'].initial = self.request.user
        
        self.fields['payee'].queryset = server_instance.members.all()
  
        self.fields['payee'].initial = self.request.user
        
    def clean(self):
        cleaned_data = super().clean()
        

        
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
        fields = ['post_name', 'description', 'split','payee', 'server', 'creator']