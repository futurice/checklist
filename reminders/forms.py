from reminders.models import ReminderList
from django import forms
from django.forms import ModelForm
import datetime

class ReminderForm(ModelForm):
    class Meta:
        model = ReminderList

