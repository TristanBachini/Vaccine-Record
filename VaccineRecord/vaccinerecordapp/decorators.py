from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):

            group = None

            if request.user.groups.exists():
                for group in request.user.groups.all():
                    groupname = group.name
                    if groupname in allowed_roles:
                        return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you may not view this page')
            
        return  wrapper_func
    return decorator