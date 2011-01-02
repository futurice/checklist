from django.conf.urls.defaults import *
import os.path

from checklist.employee.views import indexview, employeeview, employeelist, update_employeeinfo, update_employeelist, new_employee
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/checklist/listview/1'}),
#    url(r'^$', indexview, name="index", kwargs={"template_name": "index.html"}),
    url(r'listview/(?P<list_id>[0-9]+)$', employeelist, name='employeelist', kwargs={"template_name": "employeelist.html"}),
    url(r'employeeview/(?P<employee_id>[0-9]+)$', employeeview, name='employeeview', kwargs={"template_name": "employeeview.html"}),
    url(r'new_employee$', new_employee, name='new_employee', kwargs={"template_name": "new_employee.html"}),
    url(r'update/employeeinfo/(?P<employee_id>[0-9]+)$', update_employeeinfo, kwargs={"template_name": 'data_posted.html'}),
    url(r'update/employeelist/(?P<employee_id>[0-9]+)/(?P<item_id>[0-9]+)$', update_employeelist, kwargs={"template_name": 'data_posted.html'}),

    url(r'^checklist/static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),

    (r'^checklist/admin/', include(admin.site.urls)),
)
