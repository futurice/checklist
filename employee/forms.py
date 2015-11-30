from employee.models import Employee, ChecklistItem, Checklist
from django import forms
from django.forms import ModelForm
import datetime

class ItemForm(ModelForm):
    class Meta:
        model = Checklist
        exclude = ()

class DeleteForm(forms.Form):
    pass

class NewEmployee(ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'start_date', 'confirmed', 'listname', 'location', 'employee_state')
        widgets = {
            'start_date': forms.DateInput(),
        }

class EmployeeHeader(ModelForm):
    class Meta:
        model = Employee
        widgets = {
            'name': forms.TextInput(attrs={'size': 70}),
            'listname': forms.HiddenInput(),
            'deleted': forms.HiddenInput(),
            'archived': forms.HiddenInput(),
            'comments': forms.Textarea(attrs={
                'cols': 70, 'rows': 5, 'class': 'width-initial'})
        }
        exclude = ('email_notifications',)

class ListItemForm(ModelForm):
    class Meta:
        model = ChecklistItem
        widgets = {
            'itemname': forms.TextInput(attrs={'size': 90}),
            'listname': forms.HiddenInput(),
            'order': forms.HiddenInput(),
            'item_pair': forms.HiddenInput(),
        }
        exclude = ()
