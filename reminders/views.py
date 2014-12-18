from django.template import RequestContext, loader
from django.contrib.auth import get_backends
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404

from employee.models import Employee, EmployeeItem, UserPermissions
from employee.util import determine_group
from datetime import date
import json

from reminders.models import ReminderList
from reminders.forms import ReminderForm

def reminderhome(request, template_name):
    ret = {}
    unit = determine_group(request.user.username)
    if unit != "Undefined":
        ret["authorized"] = True
    lists = ReminderList.objects.all()
    ret["lists"] = lists

    return render_to_response(template_name, ret, context_instance=RequestContext(request))

def remindercreate(request, template_name):
    list = ReminderList(title="New list", content="")
    list.save()
    url = reverse("reminder_edit", kwargs={'list_id': list.id})
    return HttpResponseRedirect(url)

def reminderview(request, list_id, template_name):
    ret = {}
    alist = ReminderList.objects.get(id=list_id)
    ret["alist"] = alist
    ret["item_id"] = list_id
    ret["markdown"] = alist.markdown()
    return render_to_response(template_name, ret, context_instance=RequestContext(request))

def reminderdelete(request, list_id, template_name):
    ret = {}
    alist = ReminderList.objects.get(id=list_id)
    if request.method == 'POST':
        alist.delete()
        return HttpResponseRedirect(reverse("reminders"))
    ret["list"] = alist
    return render_to_response(template_name, ret, context_instance=RequestContext(request))

def reminderedit(request, list_id, template_name):
    ret = {}
    alist = ReminderList.objects.get(id=list_id)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=alist)
        if form.is_valid():
            form.save()
            url = reverse("reminder_view", kwargs={'list_id': alist.id})
            return HttpResponseRedirect(url)
    else:
        form = ReminderForm(instance=alist)
    ret["form"] = form
    ret["list"] = alist
    return render_to_response(template_name, ret, context_instance=RequestContext(request))
