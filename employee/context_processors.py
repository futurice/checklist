from employee.views import determine_group

def get_userinfo(request):
#    username = request.META["REMOTE_USER"]
    username = 'ojar'
    group = determine_group(username)
    return {'username': username, 'group': group}
