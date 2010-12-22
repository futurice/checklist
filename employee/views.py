from django.template import RequestContext, loader
from django.contrib.auth import get_backends
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from checklist.employee.forms import NewEmployee
from checklist.employee.models import Checklist, ChecklistItem, Employee, EmployeeItem
from datetime import datetime
import json

def indexview(request, template_name):
    lists = Checklist.objects.all()
    return render_to_response(template_name, {'lists': lists}, context_instance=RequestContext(request))

def employeelist(request, template_name, list_id):
    print list_id
    employees = Employee.objects.filter(listname=list_id)
    return render_to_response(template_name, {'employees': employees}, context_instance=RequestContext(request))

def employeeview(request, template_name, employee_id):
    employee = Employee.objects.get(id=employee_id)
    listitems = ChecklistItem.objects.filter(listname=employee.listname.id)
    employee_items = EmployeeItem.objects.filter(employee=employee)
    employee_dict = {}
    for item in employee_items:
        employee_dict[item.id] = item
    listfinished = []
    for item in listitems:
        d = {}
        if employee_dict.has_key(item.id):
            d["value"] = employee_dict[item.id].value
            d["textvalue"] = employee_dict[item.id].textvalue
        d["itemname"] = item.itemname
        d["textbox"] = item.textbox
        d["id"] = item.id
        d["unit"] = item.unit
        listfinished.append(d)
#    listitems = ChecklistItem.objects.filter(listname=list_id)
    return render_to_response(template_name, {'listitems': listfinished, 'employee': employee}, context_instance=RequestContext(request))

def getchecks(request, template_name, user_name):
    user = None
    user = EmployeeItem.objects.get(employee=1)
    keys = ["employee_id", "id", "item_id", "listname_id", "textvalue", "value"]
    output = {}
    for key in keys:
        output[key] = getattr(user, key)
    print output
    json_output = json.dumps(output)
    return render_to_response(template_name, {'json': json_output, 'user': user}, context_instance=RequestContext(request))

def update_employeelist(request, template_name, employee_id):
    employee = Employee.objects.get(id=employee_id)
    listitems = ChecklistItem.objects.filter(listname=employee.listname.id)
    items = {}
    for item in request.POST.keys():
        items[item] = request.POST[item]

    print items
    for item in listitems:
        print "----"
        print dir(item)
        (employee_item, created) = EmployeeItem.objects.get_or_create(employee=employee, item=item, listname=employee.listname)
        print "Created: %s" % created
        if "checkbox_%s" % item.id in items:
            if items["checkbox_%s" % item.id] == 'on':
                print "value true for %s" % item.id
                value = True
            else:
                print "value false for %s" % item.id
                value = False
        else:
            print "value false for %s" % item.id
            value = False

        if "textbox_%s" % item.id in items:
            print "textbox_%s = %s" % (item.id, items["textbox_%s" % item.id])
            textvalue = items["textbox_%s" % item.id]
            employee_item.textvalue = textvalue
        employee_item.value = value
        employee_item.save()

    return render_to_response(template_name, {}, context_instance=RequestContext(request))    

def update_employeeinfo(request, template_name, employee_id):
    employee = Employee.objects.get(id=employee_id)
    print dir(request)
    print dir(request.POST)
    if request.POST.has_key("confirmed"):
        if request.POST["confirmed"] == 'on':
            employee.confirmed = True
        else:
            employee.confirmed = False
    else:
        employee.confirmed = False
    employee.start_date = datetime.strptime(request.POST["date"], "%Y-%m-%d")
    print employee.start_date

    employee.save()
    return render_to_response(template_name, {}, context_instance=RequestContext(request))    

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
