from django.conf.urls.defaults import *


from checklist.employee.views import indexview, getchecks, employeeview, employeelist, update_employeeinfo, update_employeelist, new_employee
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/checklist/employee/'}),
    url(r'^checklist/$', indexview, name="index", kwargs={"template_name": "index.html"}),
    url(r'^checklist/listview/(?P<list_id>[0-9]+)$', employeelist, name='employeelist', kwargs={"template_name": "employeelist.html"}),
    url(r'^checklist/employeeview/(?P<employee_id>[0-9]+)$', employeeview, name='employeeview', kwargs={"template_name": "employeeview.html"}),
    url(r'^checklist/get/(?P<user_name>[A-Za-z0-9- ]+)$', getchecks, name='getchecks', kwargs={"template_name": "json.html"}),
    url(r'^checklist/new_employee$', new_employee, name='new_employee', kwargs={"template_name": "new_employee.html"}),
    url(r'^checklist/update/employeeinfo/(?P<employee_id>[0-9]+)$', update_employeeinfo, kwargs={"template_name": 'data_posted.html'}),
    url(r'^checklist/update/employeelist/(?P<employee_id>[0-9]+)$', update_employeelist, kwargs={"template_name": 'data_posted.html'}),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': '/home/ojar/checklist/static'}),
#    url(r'^mod/get/(?P<user_name>[A-Za-z0-9-]+)$', getjson, name="getjson", kwargs={"template_name": "getjson.html"}),

#   (r'^checklist/', include('checklist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
