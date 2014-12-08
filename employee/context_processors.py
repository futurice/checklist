from employee.views import determine_group
from employee.models import Checklist
from reminders.models import ReminderList

def get_userinfo(request):
    username = request.META["REMOTE_USER"]
    group = determine_group(username)
    return {'username': username, 'group': group}

def get_reminders(request):
    reminders = ReminderList.objects.all()
    return {'reminders': reminders}

def get_checklists(request):
    checklists = Checklist.objects.all()
    return {'checklists': checklists}
