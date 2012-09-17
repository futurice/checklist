from django.template import RequestContext, loader
from django.contrib.auth import get_backends
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
#from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from checklist.employee.forms import NewEmployee, EmployeeHeader, ListItemForm, DeleteForm
from checklist.employee.models import Checklist, ChecklistItem, Employee, EmployeeItem, UserPermissions
from datetime import date
import json



def determine_group(username):
    user = UserPermissions.objects.filter(username=username)
    for item in user:
        return item.group
    return "Undefined"

def indexview(request, template_name):
    ret = {}
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit != "Undefined":
        ret["authorized"] = True
    lists = Checklist.objects.all()
    my_items = Employee.objects.filter(ldap_account=username).order_by("start_date")
    if len(lists) > 0:
        ret["my_items"] = my_items
    ret["lists"] = lists
    return render_to_response(template_name, ret, context_instance=RequestContext(request))

def toggle_state_employee(request, action, employee_id):
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit == "Undefined":
        return render_to_response("unauthorized.html", {}, context_instance=RequestContext(request))
    employee = get_object_or_404(Employee, pk=employee_id)
    if action == "delete":
        employee.deleted = not employee.deleted
    if action == "archive":
        employee.archived = not employee.archived
    employee.save()
    return HttpResponseRedirect('/checklist/employeeview/%s' % employee.id)

def employeelist(request, template_name, list_id):
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit == "Undefined":
        return render_to_response("unauthorized.html", {}, context_instance=RequestContext(request))
    list = Checklist.objects.get(id=list_id)
    employees = Employee.objects.filter(listname=list_id,deleted=False,archived=False)
    employees_archived = Employee.objects.filter(listname=list_id,deleted=False,archived=True)

    for employee in employees:
        employee.total_count = len(ChecklistItem.objects.filter(listname=employee.listname))
        employee.done_count = len(EmployeeItem.objects.filter(employee=employee, listname=employee.listname, value=True))
        employee.your_total_count = len(ChecklistItem.objects.filter(listname=employee.listname, unit=unit))
        employee.your_done_count = len(EmployeeItem.objects.filter(employee=employee, listname=employee.listname, item__unit=unit, value=True))
        if employee.supervisor == username:
            employee.your_employee = True

    for employee in employees_archived:
        employee.total_count = len(ChecklistItem.objects.filter(listname=employee.listname))
        employee.done_count = len(EmployeeItem.objects.filter(employee=employee, listname=employee.listname, value=True))
        employee.your_total_count = len(ChecklistItem.objects.filter(listname=employee.listname, unit=unit))
        employee.your_done_count = len(EmployeeItem.objects.filter(employee=employee, listname=employee.listname, item__unit=unit, value=True))
        if employee.supervisor == username:
            employee.your_employee = True

#    (employee_item, created) = EmployeeItem.objects.get_or_create(employee=employee, item=listitem, listname=employee.listname)
 
    return render_to_response(template_name, {'listname': list.listname, 'employees': employees, 'archived': employees_archived }, context_instance=RequestContext(request))


def __combine_lists(employee_dict, items):
    listitems = []
    for item in items:
        d = {}
        if employee_dict.has_key(item.id):
            d["value"] = employee_dict[item.id].value
            d["textvalue"] = employee_dict[item.id].textvalue
        d["itemname"] = item.itemname
        d["textbox"] = item.textbox
        d["id"] = item.id
        d["unit"] = item.unit
        listitems.append(d)
    return listitems

def employeeview(request, template_name, employee_id):
    employee = Employee.objects.get(id=employee_id)
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if employee.ldap_account != username:
        if unit == "Undefined":
            return render_to_response("unauthorized.html", {}, context_instance=RequestContext(request))
    items_yours = ChecklistItem.objects.filter(listname=employee.listname.id).filter(unit=unit)
    items_others = ChecklistItem.objects.filter(listname=employee.listname.id).exclude(unit=unit)

    employee_items = EmployeeItem.objects.filter(employee=employee)
    employee_dict = {}
    for item in employee_items:
        employee_dict[item.item.id] = item

    form = EmployeeHeader(instance=employee)

    listitems_yours = __combine_lists(employee_dict, items_yours)
    listitems_others = __combine_lists(employee_dict, items_others)
    return render_to_response(template_name, {'listitems_yours': listitems_yours, 'listitems_others': listitems_others, 'employee': employee, 'employee_form': form }, context_instance=RequestContext(request))

def update_employeelist(request, template_name, employee_id, item_id):
    employee = Employee.objects.get(id=employee_id)
    listitem = ChecklistItem.objects.get(id=item_id)
    (employee_item, created) = EmployeeItem.objects.get_or_create(employee=employee, item=listitem, listname=employee.listname)
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if employee.ldap_account != username:
        if unit == "Undefined":
            return render_to_response("unauthorized.html", {}, context_instance=RequestContext(request))

    if "checkbox" in request.POST.keys():
        if request.POST["checkbox"] == 'on' or request.POST["checkbox"] == 'true' or request.POST["checkbox"] == "checked":
            employee_item.value = True
        else:
            employee_item.value = False
    else:
        employee_item.value = False
    keys = employee_item.value

    if "textbox" in request.POST.keys():
        employee_item.textvalue = request.POST["textbox"]

    employee_item.save()
    keys = {"success": True, "key": listitem.id, "employee_item_id": employee_item.id, "value": employee_item.value}
    keys = json.dumps(keys)
    return render_to_response(template_name, {"keys": keys }, context_instance=RequestContext(request))    

def update_employeeinfo(request, template_name, employee_id):
    employee = Employee.objects.get(id=employee_id)
    keys = {"success": True, "form": "headerform", "key": "header"}
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if employee.ldap_account != username:
        if unit == "Undefined":
            return render_to_response("unauthorized.html", {}, context_instance=RequestContext(request))
    if request.method == 'POST':
        formset = EmployeeHeader(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
        else:
            keys["success"] = False

    keys = json.dumps(keys)
    return render_to_response(template_name, {"keys": keys}, context_instance=RequestContext(request))    

def new_employee(request, template_name):
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit == "Undefined":
        return render_to_response("unauthorized.html", {}, context_instance=RequestContext(request))
    if request.method == 'POST': # If the form has been submitted...
        form = NewEmployee(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            employee = form.save(commit=False)
            employee.save()
            return HttpResponseRedirect('/checklist/employeeview/%s' % employee.id) # Redirect after POST
    else:
        form = NewEmployee() # An unbound form

    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))    


