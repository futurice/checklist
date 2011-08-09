from employee.models import Checklist, ChecklistItem, Employee, EmployeeItem, Checkpoint
from django.contrib import admin

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ['listname']

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['listname', 'itemname', 'unit']
    list_filter = ('listname', 'unit')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["listname", "name", "start_date"]
    list_filter = ("archived",)

class CheckpointAdmin(admin.ModelAdmin):
    pass

admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeItem)
admin.site.register(Checkpoint, CheckpointAdmin)

