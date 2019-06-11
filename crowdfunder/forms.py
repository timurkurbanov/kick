from django.forms import CharField, PasswordInput, Form, ModelForm
from django import forms
from crowdfunder.models import Project
from datetime import date, datetime
from django.core.exceptions import ValidationError
from pytz import timezone
from crowdfunder.models import *

import datetime as dt

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class CreateProject(ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': dt.date.today() }))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': dt.date.today() }))

    class Meta:
        model = Project
        fields = [
            'title',
            'picture',
            'description',
            'category',
            'funding_goal',
            'start_date',
            'end_date',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Your project title'}),
            'picture': forms.URLInput(attrs={'placeholder': 'Picture url'}),
            'description': forms.Textarea(attrs={'placeholder': 'Your project description'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']

        if start_date > end_date:
            raise forms.ValidationError('End date must be later than the start date!')
        

class AddRewardForm(ModelForm):
    class Meta:
        model = Reward
        fields = [
            'name',
            'description',
            'donation_value',
            'cap',
            'project',
        ]
        widgets = {
            'project': forms.HiddenInput()
        }


class MakeDonation(ModelForm):
    class Meta:
        model = Donation
        fields = [
            'user',
            'project',
            'donation_amount',
        ]
        widgets = {
            'user': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        donation_user = cleaned_data.get("user")
        project = cleaned_data.get("project")

        if donation_user == project.owner:
            raise forms.ValidationError("You cannot donate to your own project!")

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'user',
            'project',
            'message'
        ]
        widgets = {
            'user': forms.HiddenInput(),
            'project': forms.HiddenInput()
        }


   