from employee.models import Checklist, ChecklistItem, Employee, EmployeeItem, Checkpoint, UserPermissions
from django.contrib import admin

def check_permission(aself, request, group):
    if request.user.is_superuser:
        return True
    try:
        user = UserPermissions.objects.filter(username=request.user.username)
        for item in user:
            if item.group in group:
                return True
    except:
        return False
    return False

class AdminBase(admin.ModelAdmin):
    def has_add_permission(self, request):
        return check_permission(self, request, self.required_group)

    def has_change_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

    def has_delete_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

class UserPermissionsAdmin(AdminBase):
    list_display = ['username', 'group']
    list_filter = ['group']
    required_group = ["IT", "HR", "SU"]

class ChecklistAdmin(AdminBase):
    list_display = ['listname']
    required_group = ["IT"]

class ChecklistItemAdmin(AdminBase):
    list_display = ['listname', 'itemname', 'unit']
    list_filter = ('listname', 'unit')
    required_group = ["IT"]

class EmployeeAdmin(AdminBase):
    list_display = ["listname", "name", "start_date"]
    list_filter = ("archived",)
    required_group = ["IT"]

class CheckpointAdmin(AdminBase):
    required_group = ["IT"]

admin.site.register(UserPermissions, UserPermissionsAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeItem)
admin.site.register(Checkpoint, CheckpointAdmin)
