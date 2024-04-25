from django import forms
from posts.models import RecurringTask
from users.models import User
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from servers.models import Server

class RecurringTaskForm(forms.ModelForm):
    recurring_unit = forms.ChoiceField(choices=RecurringTask.FREQUENCY_CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.server_instance = kwargs.pop('server_instance', None)
        super(RecurringTaskForm, self).__init__(*args, **kwargs)
        
        members = self.server_instance.members.all()
        self.fields['assignee'].choices = [(member.id, member.display_name(self.server_instance)) for member in members]
        self.fields['first_due_date'].initial = datetime.datetime.now().strftime('%Y-%m-%d')

        # label for recurring_period
        self.fields['first_due_date'].label = 'First time the task is due'

        
    #def clean(self):
    #    cleaned_data = super().clean()
    #    # validation if needed can go here
    #    return cleaned_data
    class Meta:
        model = RecurringTask
        fields = ['title', 'description', 'assignee', 'first_due_date', 'recurring_unit', 'recurring_period']
        widgets = {
            'first_due_date':forms.TextInput(attrs={'type':'datetime-local'}),
            'assignee':forms.CheckboxSelectMultiple(),
        }


is_htmx = lambda request: request.headers.get('HX-Request', False)
def create_recurring_task(request, server_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    server_instance = Server.objects.get(pk=server_id)
    if request.method == 'POST':
        form = RecurringTaskForm(request.POST, server_instance=server_instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.server = server_instance
            obj.creator = request.user
            obj.save()
            form.save_m2m()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            return render(request, 'servers/partials/recurring-task-form.html', {
                'form': form,
                'server_id': server_id,
            })
    
    form = RecurringTaskForm(server_instance=server_instance)
    return render(request, 'servers/partials/recurring-task-form.html', {
        'form': form,
        'server_id': server_instance.id,
    })

