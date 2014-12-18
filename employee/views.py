from django.template import RequestContext, loader
from django.contrib.auth import get_backends
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import redirect, render, render_to_response, get_object_or_404

from employee.forms import NewEmployee, EmployeeHeader, ListItemForm, DeleteForm
from employee.models import Checklist, ChecklistItem, Employee, EmployeeItem, UserPermissions
from employee.util import determine_group

from datetime import date
import itertools
import json


def fill_employee_extra(employee, viewer_username, viewer_unit):
    """
    Add extra fields to the Employee object.

    employee - Employee object
    viewer_username - the username of the viewer (performing the web request)
    viewer_unit - string returned by determine_group(...)
    """
    employee.total_count = ChecklistItem.objects.filter(listname=employee.listname).count()
    employee.done_count = EmployeeItem.objects.filter(employee=employee, listname=employee.listname, value=True).count()
    employee.your_total_count = ChecklistItem.objects.filter(listname=employee.listname, unit=viewer_unit).count()
    employee.your_done_count = EmployeeItem.objects.filter(employee=employee, listname=employee.listname, item__unit=viewer_unit, value=True).count()
    if employee.supervisor == viewer_username:
        employee.your_employee = True

def indexview(request):
    ret = {}
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit != "Undefined":
        ret["authorized"] = True
    lists = Checklist.objects.all()
    my_items = Employee.objects.filter(ldap_account=request.user.username).order_by("start_date")
    ret["my_items"] = my_items
    ret["lists"] = lists

    all_employees = Employee.objects.filter(deleted=False)
    employees_unarchived = all_employees.filter(archived=False)
    employees_archived = all_employees.filter(archived=True)
    for employee in itertools.chain(employees_unarchived, employees_archived):
        fill_employee_extra(employee, username, unit)
    ret['employees'] = employees_unarchived
    ret['archived'] = employees_archived

    return render(request, 'index.html', ret)

def toggle_state_employee(request, action, employee_id):
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit == "Undefined":
        return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
    employee = get_object_or_404(Employee, pk=employee_id)
    if action == "delete":
        employee.deleted = not employee.deleted
    if action == "archive":
        employee.archived = not employee.archived
    employee.save()
    url = reverse('employeeview', kwargs={'employee_id': employee.id})
    return HttpResponseRedirect(url)

def employeelist(request, template_name, list_id, without_item_id=None):
    username = request.META["REMOTE_USER"]
    unit = determine_group(username)
    if unit == "Undefined":
        return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
    chklist = Checklist.objects.get(id=list_id)
    all_employees = Employee.objects.filter(listname=list_id, deleted=False)

    # exclude employees who have this item ticked
    without_item = None
    if without_item_id is not None:
        without_item = ChecklistItem.objects.get(id=without_item_id)
        empl_id_with_item = all_employees.filter(
                employeeitem__item_id=without_item_id,
                employeeitem__value=True).values('id')
        all_employees = all_employees.exclude(id__in=empl_id_with_item)

    employees_unarchived = all_employees.filter(archived=False)
    employees_archived = all_employees.filter(archived=True)

    for employee in itertools.chain(employees_unarchived, employees_archived):
        fill_employee_extra(employee, username, unit)
        try:
            employee.textvalue = EmployeeItem.objects.get(
                    employee_id=employee.id, item=without_item,
                    listname=employee.listname).textvalue
        except EmployeeItem.DoesNotExist:
            pass

    return render_to_response(template_name, {
        'chklist': chklist,
        'employees': employees_unarchived,
        'archived': employees_archived,
        'without_item': without_item,
        'without_item_url': reverse('employeelist',
            kwargs={'list_id': chklist.id}),
    }, context_instance=RequestContext(request))


def __combine_lists(employee_dict, items):
    listitems = []
    for item in items:
        d = {}
        if employee_dict.has_key(item.id):
            d["value"] = employee_dict[item.id].value
            d["textvalue"] = employee_dict[item.id].textvalue
        d["itemname"] = item.itemname
        d["markdown_itemname"] = item.markdown_itemname()
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
            return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
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
            return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))

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
            return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
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
        return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
    if request.method == 'POST': # If the form has been submitted...
        form = NewEmployee(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            employee = form.save(commit=False)
            employee.save()
            url = reverse('employeeview', kwargs={'employee_id': employee.id})
            return HttpResponseRedirect(url) # Redirect after POST
    else:
        form = NewEmployee() # An unbound form

    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))


