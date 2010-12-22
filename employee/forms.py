from django import forms
import datetime
class NewEmployee(forms.Form):
    name = forms.CharField(max_length=100)
    confirmed = forms.BooleanField(required=False)
    start_date = forms.DateField(initial=datetime.date.today)
