from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http.response import JsonResponse


def is_admin(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

            if request.user.is_admin == True:
                messages.info(request, 'َشما هم اکنون در صفحه مدیریت با دسترسی مدیر هستید.', extra_tags='secondary')
                return function(request, *args, **kwargs)
            else:
                messages.error(request, 'این صفحه وجود ندارد', extra_tags='danger')
                return redirect('home_url')

    return wrap

def is_get(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.method == 'GET':
            return view(request, *args, **kwargs)
        return JsonResponse({'error':'you can only access with get method'}, status=200)
    
    return wrapper

def is_post(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return view(request, *args, **kwargs)
        return JsonResponse({'error':'you can only access with post method'}, status=200)
    
    return wrapper


def login_required(view):
    @wraps(view)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request,*args, **kwargs)
        else:
            messages.error(request, 'برای دسترسی به این صفحه شما نیاز دارید به حساب کاربری خود وارد شوید.', extra_tags="danger")
            return redirect('home_url')
    return wrap