from django import forms
from .models import Server
class EmailForm(forms.Form):
    emails = forms.CharField(label='Emails', widget=forms.Textarea(attrs={'placeholder': 'Enter one or more emails separated by commas'}))

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['group_name',]