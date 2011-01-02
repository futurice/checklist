from employee.models import Employee, ChecklistItem
from django import forms
from django.forms import ModelForm
import datetime

class NewEmployee(ModelForm):
#    name = forms.CharField(max_length=100)
#    confirmed = forms.BooleanField(required=False)
#    start_date = forms.DateField(initial=datetime.date.today)
    class Meta:
        model = Employee
        fields = ('name', 'start_date', 'confirmed', 'listname')
        widgets = {
            'start_date': forms.DateInput(),
        }

class EmployeeHeader(ModelForm):
    class Meta:
        model = Employee
#        fields = ('name', 'start_date', 'confirmed', 'archived', 'supervisor', 'email', 'email_notifications', 'phone', 'comments', 'id', 'listname', 'deleted')
        widgets = {
            'name': forms.TextInput(attrs={'size': 70}),
            'listname': forms.HiddenInput(),
            'deleted': forms.HiddenInput(),
            'archived': forms.HiddenInput(),
            'comments': forms.Textarea(attrs={'cols': 70, 'rows': 5})
        }

class ListItemForm(ModelForm):
    class Meta:
        model = ChecklistItem
        widgets = {
            'listname': forms.HiddenInput(),
            'item_pair': forms.HiddenInput(),
        }
