from django.template import RequestContext, loader
from django.contrib.auth import get_backends
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
#from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from employee.forms import NewEmployee, EmployeeHeader, ListItemForm, DeleteForm
from django.forms.models import modelformset_factory

from employee.models import Checklist, ChecklistItem, Employee, EmployeeItem
from employee.util import determine_group
from datetime import date
import json

ListItemFormset = modelformset_factory(ChecklistItem, fields=("order",))

def edit_lists(request, template_name):
    unit = determine_group(request.user.username)
    if unit == "Undefined":
        return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
    lists = Checklist.objects.all()
    return render_to_response(template_name, {"lists": lists}, context_instance=RequestContext(request))

def edit_list(request, list_id, template_name):
    unit = determine_group(request.user.username)
    if unit == "Undefined":
        return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
    list = Checklist.objects.get(id=list_id)
    if request.method == 'POST':
        formset = ListItemFormset(request.POST, queryset=ChecklistItem.objects.filter(listname=list))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    obj = ChecklistItem.objects.get(id=instance.id)
                    obj.order = instance.order
                    obj.save()
                except:
                    pass
    form = ListItemFormset(queryset=ChecklistItem.objects.filter(listname=list))
    items = ChecklistItem.objects.filter(listname=list).order_by("order")
    return render_to_response(template_name, {"list": list, "items": items, "form": form}, context_instance=RequestContext(request))

def edit_list_item(request, action, item_id, list_id, template_name):
    unit = determine_group(request.user.username)
    if unit == "Undefined":
        return render_to_response("common/unauthorized.html", {}, context_instance=RequestContext(request))
    list = Checklist.objects.get(id=list_id)
    if request.method == 'POST':
        if request.GET.get("action") == "delete":
            form = DeleteForm(request.POST)
            if form.is_valid():
                ChecklistItem.objects.get(id=item_id).delete()
                url = reverse("edit_list", kwargs = {'list_id': list_id})
                return HttpResponseRedirect(url)
            else:
                return HttpResponse404()
        try:
            if action == 'pair':
                instance = ChecklistItem.objects.get(item_pair=item_id)
            else:
                instance = ChecklistItem.objects.get(id=item_id)
            form = ListItemForm(request.POST, instance=instance)
        except ObjectDoesNotExist:
            form = ListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.listname = list
            if action == 'new':
                try:
                    largest_order = ChecklistItem.objects.filter(listname=list).order_by("-order")[0].order
                    item.order = largest_order + 1
                except:
                    largest_order = 0
                item.save()
                url = reverse("edit_list_item", kwargs = {
                    'list_id': list_id,
                    'item_id': item.id,
                })
                return HttpResponseRedirect(url)
            item.save()

    else:
        if action == 'new':
            form = ListItemForm(initial={"listname": list_id, "order": 0})
        elif action == 'pair':
            try:
                instance = ChecklistItem.objects.get(item_pair=item_id)
            except ObjectDoesNotExist:
                instance = ChecklistItem(itemname='Item name', unit='Unit name', order=20, listname=Checklist.objects.get(id=2), item_pair=ChecklistItem.objects.get(id=item_id))
            form = ListItemForm(instance=instance)
        else: # action = edit
            instance = ChecklistItem.objects.get(id=item_id)
            form = ListItemForm(instance=instance)

    return render_to_response(template_name, {'form': form, "list_id": list.id}, context_instance=RequestContext(request))


