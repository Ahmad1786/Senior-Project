from django import forms
from .models import Chore

class SwapOfferForm(forms.Form):
    chores = forms.ModelChoiceField(queryset=Chore.objects.none(), empty_label=None)
    action = forms.ChoiceField(choices=[('take_task', 'Just take the task'), ('make_offer', 'Make swap offer')])

    def __init__(self, user, *args, **kwargs):
        super(SwapOfferForm, self).__init__(*args, **kwargs)
        self.fields['chores'].queryset = Chore.objects.filter(assignee=user)

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        if action == 'make_offer' and not cleaned_data.get('chores'):
            raise forms.ValidationError('Please select a chore to offer in the swap.')
        return cleaned_data

