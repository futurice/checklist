from employee.views import determine_group
from employee.models import Checklist
from reminders.models import ReminderList

def get_userinfo(request):
    group = determine_group(request.user.username)
    return {'username': request.user.username, 'group': group}

def get_reminders(request):
    reminders = ReminderList.objects.all()
    return {'reminders': reminders}

def get_checklists(request):
    checklists = Checklist.objects.all()
    return {'checklists': checklists}
