from django import forms

class EmailForm(forms.Form):
    emails = forms.CharField(label='Emails', widget=forms.Textarea(attrs={'placeholder': 'Enter one or more emails separated by commas'}))
