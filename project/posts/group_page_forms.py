from django import forms

from posts.models import Bill, Event, Chore, Comment
from servers.models import Invitation, Participation
import datetime

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Remove all but content when done with testing.
        fields = ["author", "task", "event", "bill", "parent_comment", "content",]
        widgets = {
            "content": forms.TextInput(attrs={'class': 'form-control'}),
        }


class BillForm(forms.ModelForm):
    payers = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):
        self.server_instance = kwargs.pop('server_instance', None)
        self.current_user = kwargs.pop('current_user', None)
        super(BillForm, self).__init__(*args, **kwargs)
        
        members = self.server_instance.members.all()
        self.fields['payers'].queryset = members
        #self.fields['payers'].choices = [(member.id, member.display_name(self.server_instance)) for member in members]
        #self.fields['payers'].choices = [member.display_name(self.server_instance) for member in members]
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
    assignee = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.server_instance = kwargs.pop('server_instance', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        members = self.server_instance.members.all()
        self.fields['assignee'].queryset = members
        #self.fields['assignee'].choices = [(member.id, member.display_name(self.server_instance)) for member in members]
        self.fields['due_date'].initial = datetime.datetime.now().strftime('%Y-%m-%d')
        
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
        
    class Meta:
        model = Event
        fields = ['post_name', 'description', 'date_time']
        widgets = {
            'date_time':forms.TextInput(attrs={'type':'datetime-local'}),
        }

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['post_name', 'description', 'date_time']
        widgets = {
            'date_time':forms.TextInput(attrs={'type':'datetime-local'}),
        }

class EditBillForm(forms.ModelForm):
    payers = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        super(EditBillForm, self).__init__(*args, **kwargs)

        members = self.instance.server.members.all()
        self.fields['payers'].queryset = members
        #self.fields['payers'].choices = [(member.id, member.display_name(self.instance.server)) for member in members]

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

    class Meta:
        model = Bill
        fields = ['post_name', 'description', 'cost', 'split', 'payers']


class EditTaskForm(forms.ModelForm):
    assignee = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)

        members = self.instance.server.members.all()
        self.fields['assignee'].queryset = members
        #self.fields['assignee'].choices = [(member.id, member.display_name(self.instance.server)) for member in members]
        
    class Meta:
        model = Chore
        fields = ['post_name', 'description', 'assignee', 'due_date']
        widgets = {
            'due_date':forms.TextInput(attrs={'type':'date'}),
        }


class AssignTaskForm(forms.ModelForm):
    task_id = forms.ModelChoiceField(queryset=None, empty_label=None, label="Select Task")
    assigned_users = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Chore
        fields = ['task_id', 'assigned_users']
        
    def __init__(self, *args, **kwargs):
        super(AssignTaskForm, self).__init__(*args, **kwargs)
        self.fields['task_id'].queryset = Chore.objects.all() 
        self.fields['assigned_users'].queryset = self.instance.server.members.all()
       

class InvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        server_instance = kwargs.pop('server_instance', None)
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.server_instance = server_instance

    def clean_invited_email(self):
        invited_email = self.cleaned_data.get('invited_email')
        if Participation.objects.filter(server=self.server_instance, user__email=invited_email).exists():
            raise forms.ValidationError("This email is already associated with a user participating in the server.")
        return invited_email

    class Meta:
        model = Invitation
        fields = ['invited_email']


# form for leaderboard 
class LeaderboardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LeaderboardForm, self).__init__(*args, **kwargs)

        users_with_points = Participation.objects.all().values_list('display_name', 'points')

        leaderboard_text = '\n'.join([f"{display_name}: {points}" for display_name, points in users_with_points])
        
        self.fields['leaderboard'] = forms.CharField(initial=leaderboard_text, widget=forms.Textarea(attrs={'readonly': 'readonly'}))

# form for completing tasks
class CompleteTaskForm(forms.ModelForm):
    task_id = forms.ModelChoiceField(queryset=None, empty_label=None, label="Select task you have completed")
    class Meta:
        model = Chore
        fields = ['task_id']
        
    def __init__(self, *args, **kwargs):
        super(CompleteTaskForm, self).__init__(*args, **kwargs)
        self.fields['task_id'].queryset = Chore.objects.all() 
       
