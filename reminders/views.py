from django.template import RequestContext, loader
from django.contrib.auth import get_backends
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404

from employee.models import Employee, EmployeeItem, UserPermissions
from datetime import date
import json

from reminders.models import ReminderList
from reminders.forms import ReminderForm

def determine_group(username):
    user = UserPermissions.objects.filter(username=username)
    for item in user:
        return item.group
    return "Undefined"

def reminderhome(request, template_name):
    ret = {}
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit != "Undefined":
        ret["authorized"] = True
    lists = ReminderList.objects.all()
    ret["lists"] = lists

    return render_to_response(template_name, ret, context_instance=RequestContext(request))

def remindercreate(request, template_name):
    list = ReminderList(title="New list", content="")
    list.save()
    return HttpResponseRedirect("/checklist/reminders/edit/%s" % list.id)

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
        return HttpResponseRedirect("/checklist/reminders")
    ret["list"] = alist
    return render_to_response(template_name, ret, context_instance=RequestContext(request))

def reminderedit(request, list_id, template_name):
    ret = {}
    alist = ReminderList.objects.get(id=list_id)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=alist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/checklist/reminders/%s" % alist.id)
    else:
        form = ReminderForm(instance=alist)
    ret["form"] = form
    ret["list"] = alist
    return render_to_response(template_name, ret, context_instance=RequestContext(request))
