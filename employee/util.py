from models import UserPermissions

def determine_group(username):
    user = UserPermissions.objects.filter(username=username)
    for item in user:
        return item.group
    return "Undefined"
