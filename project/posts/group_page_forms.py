# THESE ARE THE INITIAL FORMS FOR THE SERVERS APP
# THESE WILL BE USED TO MAKE an instance of THE 3 MAIN POSTS IN THE GROUP PAGE

from django import forms
from posts.models import Bill, Event, Chore, Comment
import datetime

# NOTE: MADE these forms kind of "fast", so they may not be the 
# best/most efficient way to do things, but good enough for now
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.TextInput(attrs={'class': 'form-control'}),
        }


class BillForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.server_instance = kwargs.pop('server_instance', None)
        self.current_user = kwargs.pop('current_user', None)
        super(BillForm, self).__init__(*args, **kwargs)
        
        members = self.server_instance.members.all()
        #self.fields['payers'].queryset = members
        self.fields['payers'].choices = [(member.id, member.display_name(self.server_instance)) for member in members]
        self.fields['payers'].initial = self.current_user
        
    def clean(self):
        cleaned_data = super().clean()
        
        # currently allowing for cost of 0 but not empty
        if cleaned_data.get('cost', None) is None:
            self.add_error('cost', 'There must be a cost for the bill')

        if cleaned_data.get('cost', None) is not None and cleaned_data['cost'] < 0:
            self.add_error('cost', 'The cost must be a positive value')
        
        if not cleaned_data['split'] and len(cleaned_data['payers']) > 1:
            self.add_error('payers', 'Can not split bill between multiple people if split is not checked')

        if cleaned_data['split'] and len(cleaned_data['payers']) == 1:
            self.add_error('payers', 'Must split bill between multiple people if split is checked')

        # Decided this may not be what we want but basically i was trying to say
        # if split is false: the user making the post must be the only one paying
        # if not cleaned_data['split']:
        #    print(cleaned_data['payers'])
        #    print(self.request.user)
        #    cleaned_data['payers'] = [self.request.user]
        
        return cleaned_data

    class Meta:
        model = Bill
        fields = ['post_name', 'description', 'cost', 'split', 'payers']


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.server_instance = kwargs.pop('server_instance', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        members = self.server_instance.members.all()
        # self.fields['assignee'].queryset = members
        self.fields['assignee'].choices = [(member.id, member.display_name(self.server_instance)) for member in members]
        self.fields['due_date'].initial = datetime.datetime.now().strftime('%Y-%m-%d')
        
    #def clean(self):
    #    cleaned_data = super().clean()
    #    # validation if needed can go here
    #    return cleaned_data
    class Meta:
        model = Chore
        fields = ['post_name', 'description', 'assignee', 'due_date']
        widgets = {
            'due_date':forms.TextInput(attrs={'type':'date'}),
        }


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        
        # label for datetime
        self.fields['date_time'].label = "Date and Time"
        self.fields['date_time'].initial = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        
    #def clean(self):
    #    cleaned_data = super().clean()
    #    # validation if needed can go here
    #    return cleaned_data"""

    class Meta:
        model = Event
        fields = ['post_name', 'description', 'date_time']
        widgets = {
            'date_time':forms.TextInput(attrs={'type':'datetime-local'}),
        }

# Function for editing event form - done by Luke
class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['post_name', 'description', 'date_time']
        widgets = {
            'date_time':forms.TextInput(attrs={'type':'datetime-local'}),
        }

# Function for editing the bill form - done by Luke
class EditBillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditBillForm, self).__init__(*args, **kwargs)

        members = self.instance.server.members.all()
        #self.fields['payers'].queryset = members
        self.fields['payers'].choices = [(member.id, member.display_name(self.instance.server)) for member in members]

    class Meta:
        model = Bill
        fields = ['post_name', 'description', 'cost', 'split', 'payers']

# Function for editing the task form - done by Luke
class EditTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)

        members = self.instance.server.members.all()
        # self.fields['assignee'].queryset = members
        self.fields['assignee'].choices = [(member.id, member.display_name(self.instance.server)) for member in members]
        
    class Meta:
        model = Chore
        fields = ['post_name', 'description', 'assignee', 'due_date']
        widgets = {
            'due_date':forms.TextInput(attrs={'type':'date'}),
        }
