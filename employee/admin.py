from employee.models import Checklist, ChecklistItem, Employee, EmployeeItem, Checkpoint, UserPermissions
from django.contrib import admin

def check_permission(aself, request, group):
    try:
        user = UserPermissions.objects.filter(username=request.user.username)
        for item in user:
            if item.group in group:
                return True
    except:
        return False
    return False

class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ['username', 'group']
    list_filter = ['group']
    required_group = ["IT", "HR", "SU"]

    def has_add_permission(self, request):
        return check_permission(self, request, self.required_group)

    def has_change_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

    def has_delete_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ['listname']
    required_group = ["IT"]

    def has_add_permission(self, request):
        return check_permission(self, request, self.required_group)

    def has_change_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

    def has_delete_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['listname', 'itemname', 'unit']
    list_filter = ('listname', 'unit')
    required_group = ["IT"]

    def has_add_permission(self, request):
        return check_permission(self, request, self.required_group)

    def has_change_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

    def has_delete_permission(self, request, *args):
        return check_permission(self, request, self.required_group)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["listname", "name", "start_date"]
    list_filter = ("archived",)
    required_group = ["IT"]

    def has_add_permission(self, request):
        return check_permission(self, request, self.required_group)

    def has_change_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

    def has_delete_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

class CheckpointAdmin(admin.ModelAdmin):
    required_group = ["IT"]

    def has_add_permission(self, request):
        return check_permission(self, request, self.required_group)

    def has_change_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

    def has_delete_permission(self, request, *args):
        return check_permission(self, request, self.required_group)

admin.site.register(UserPermissions, UserPermissionsAdmin)

admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeItem)
admin.site.register(Checkpoint, CheckpointAdmin)
