from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps
from django.views.decorators.cache import never_cache
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    @never_cache
    @login_required
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "No eres admin.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def empresa_required(view_func):
    @wraps(view_func)
    @never_cache
    @login_required
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_empresa:
            messages.error(request, "No eres empresa.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func