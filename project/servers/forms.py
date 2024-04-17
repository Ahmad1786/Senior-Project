from django import forms
from posts.models import SwapOffer
from posts.models import Chore

class EmailForm(forms.Form):
    emails = forms.CharField(label='Emails', widget=forms.Textarea(attrs={'placeholder': 'Enter one or more emails separated by commas'}))


class SwapOfferForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('', 'Choose...'),  # Default/placeholder option
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined')
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    class Meta:
        model = SwapOffer
        fields = ['offer_chore', 'status']  # Include the status field in the form

    def __init__(self, *args, user, swap_request, **kwargs):
        super(SwapOfferForm, self).__init__(*args, **kwargs)
        server = swap_request.chore.server  # Server associated with the swap request

        # Setting up the queryset for offer_chore
        self.fields['offer_chore'].queryset = Chore.objects.filter(
            server=server,
            assignee=user
        ).exclude(
            assignee=swap_request.requester
        )
        self.fields['offer_chore'].required = False
        self.fields['offer_chore'].empty_label = 'None'  # Optional: Set a label for the "None" option
        self.fields['status'].required = True
        # Optionally, initialize the status field.
        if 'initial' in kwargs:
            self.fields['status'].initial = kwargs['initial'].get('status', '')
