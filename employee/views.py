from django.template import RequestContext, loader
from django.contrib.auth import get_backends
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from checklist.employee.forms import NewEmployee
from checklist.employee.models import Checklist, ChecklistItem, Employee, EmployeeItem
from datetime import datetime
import json

def determine_group(username):
    if username in ["ojar", "valh", "mmal", "lekl", "spiq", "lrom"]:
        return "IT"
    if username in ["ltan"]:
        return "Lotta"
    if username in ["srot", "llem", "pjal", "aker"]:
        return "HR"
    return "Supervisor"

def indexview(request, template_name):
    lists = Checklist.objects.all()
    return render_to_response(template_name, {'lists': lists}, context_instance=RequestContext(request))

def employeelist(request, template_name, list_id):
    print list_id
    employees = Employee.objects.filter(listname=list_id,deleted=False,archived=False)
    employees_archived = Employee.objects.filter(listname=list_id,deleted=False,archived=True)
    return render_to_response(template_name, {'employees': employees, 'archived': employees_archived }, context_instance=RequestContext(request))


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
    unit = determine_group("ojar")
    items_yours = ChecklistItem.objects.filter(listname=employee.listname.id).filter(unit=unit)
    items_others = ChecklistItem.objects.filter(listname=employee.listname.id).exclude(unit=unit)

    employee_items = EmployeeItem.objects.filter(employee=employee)
    employee_dict = {}
    for item in employee_items:
        employee_dict[item.item.id] = item

    listitems_yours = __combine_lists(employee_dict, items_yours)
    listitems_others = __combine_lists(employee_dict, items_others)
    print listitems_yours
    print listitems_others
#    listitems = ChecklistItem.objects.filter(listname=list_id)
    return render_to_response(template_name, {'listitems_yours': listitems_yours, 'listitems_others': listitems_others, 'employee': employee}, context_instance=RequestContext(request))

def update_employeelist(request, template_name, employee_id, item_id):
    employee = Employee.objects.get(id=employee_id)
    listitem = ChecklistItem.objects.get(id=item_id)
    (employee_item, created) = EmployeeItem.objects.get_or_create(employee=employee, item=listitem, listname=employee.listname)
    keys = ""
    print request.POST.keys()
    if "checkbox" in request.POST.keys():
        print "Checkbox value: %s" % request.POST["checkbox"]
        if request.POST["checkbox"] == 'on' or request.POST["checkbox"] == 'true':
            employee_item.value = True
            keys = "value = true"
        else:
            employee_item.value = False
    else:
        employee_item.value = False
    keys = employee_item.value

    if "textbox" in request.POST.keys():
        employee_item.textvalue = request.POST["textbox"]
        print "Textvalue: %s" % employee_item.textvalue
    employee_item.save()
    keys = {"success": True, "key": listitem.id, "employee_item_id": employee_item.id, "value": employee_item.value}
    keys = json.dumps(keys)
    return render_to_response(template_name, {"keys": keys }, context_instance=RequestContext(request))    

def update_employeeinfo(request, template_name, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.POST.has_key("confirmed"):
        if request.POST["confirmed"] == 'on' or request.POST["confirmed"] == "true":
            employee.confirmed = True
        else:
            employee.confirmed = False
    else:
        employee.confirmed = False
    if request.POST.has_key("archived"):
        if request.POST["archived"] == 'on' or request.POST["archived"] == "true":
            employee.archived = True
        else:
            employee.archived = False
    else:
        employee.archived = False
    if request.POST.has_key("date"):
        employee.start_date = datetime.strptime(request.POST["date"], "%Y-%m-%d")
    if request.POST.has_key("comments"):
        employee.comments = request.POST["comments"]
    if request.POST.has_key("supervisor"):
        employee.supervisor = request.POST["supervisor"]

    employee.save()
    keys = {"success": True, "form": "headerform", "key": "header"}
    keys = json.dumps(keys)
    return render_to_response(template_name, {"keys": keys}, context_instance=RequestContext(request))    

def new_employee(request, template_name):
    if request.method == 'POST': # If the form has been submitted...
        form = NewEmployee(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            checklist = Checklist.objects.get(id=1)
            employee = Employee(name=form.cleaned_data['name'], listname=checklist, start_date=form.cleaned_data["start_date"], confirmed=form.cleaned_data["confirmed"])
            employee.save()
            return HttpResponseRedirect('/checklist/employeeview/%s' % employee.id) # Redirect after POST
    else:
        form = NewEmployee() # An unbound form

    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))    
