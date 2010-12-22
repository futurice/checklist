from employee.models import Checklist, ChecklistItem, Employee, EmployeeItem
from django.contrib import admin

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ['listname']

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['listname', 'itemname']

admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Employee)
admin.site.register(EmployeeItem)

