from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('mainpage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.group.name == allowed_roles[0]:
                return view_func(request, *args, **kwargs)
            if request.user.group.name == 'staff':
                return redirect('staff_page')
            else:
                return HttpResponse("Unauthorized access!")
        return wrapper_func
    return decorator
