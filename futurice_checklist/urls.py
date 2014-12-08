from django.conf.urls import patterns, include, url
from django.contrib import admin

import os.path
from employee.views import indexview, employeeview, employeelist, update_employeeinfo, update_employeelist, new_employee, toggle_state_employee
from editlist.views import edit_lists, edit_list, edit_list_item
from reminders.views import reminderhome, remindercreate, reminderedit, reminderview, reminderdelete

urlpatterns = patterns('',
    url(r'^$', indexview, name="index"),
    url(r'^listview/(?P<list_id>[0-9]+)$', employeelist, name='employeelist', kwargs={"template_name": "employeelist.html"}),
    url(r'^employeeview/(?P<employee_id>[0-9]+)$', employeeview, name='employeeview', kwargs={"template_name": "employeeview.html"}),
    url(r'^new_employee$', new_employee, name='new_employee', kwargs={"template_name": "new_employee.html"}),
    url(r'^update/employee/state/(?P<action>[a-z]+)/(?P<employee_id>[0-9]+)$', toggle_state_employee, name="x_employee"),
    url(r'^update/employeeinfo/(?P<employee_id>[0-9]+)$', update_employeeinfo, kwargs={"template_name": 'data_posted.html'}, name="update_info"),
    url(r'^update/employeelist/(?P<employee_id>[0-9]+)/(?P<item_id>[0-9]+)$', update_employeelist, kwargs={"template_name": 'data_posted.html'}, name="update_employee"),

    url(r'^edit/(?P<list_id>[0-9]+)/add$', edit_list_item, kwargs={"template_name": "edit_list_item.html", "action": "new", "item_id": 0}, name="edit_check"),
    url(r'^edit/(?P<list_id>[0-9]+)/edit/(?P<item_id>[0-9]+)$', edit_list_item, kwargs={"template_name": "edit_list_item.html", "action": "edit"}, name="edit_list_item"),
    url(r'^edit/(?P<list_id>[0-9]+)$', edit_list, kwargs={"template_name": "edit_list.html"}, name="edit_list"),
    url(r'^edit$', edit_lists, kwargs={"template_name": "edit_lists.html"}, name="edit"),

    url(r'^reminders$', reminderhome, kwargs={"template_name": "home.html"}, name="reminders"),
    url(r'^reminders/create$', remindercreate, kwargs={"template_name": "edit.html"}, name="reminder_create"),
    url(r'^reminders/edit/(?P<list_id>[0-9]+)$', reminderedit, kwargs={"template_name": "edit.html"}, name="reminder_edit"),
    url(r'^reminders/delete/(?P<list_id>[0-9]+)$', reminderdelete, kwargs={"template_name": "reminders/delete.html"}, name="reminder_delete"),
    url(r'^reminders/(?P<list_id>[0-9]+)$', reminderview, kwargs={"template_name": "view.html"}, name="reminder_view"),

    url(r'^checklist/static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),

    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#reversing-admin-urls
    url(r'^admin/', include(admin.site.urls)),
)
