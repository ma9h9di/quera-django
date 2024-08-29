from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, Resolver404

EXEMPT_URLS = [
    'finance:user:login',  # Add the name of your login URL
    'finance:user:signup',  # Add the name of your signup URL if you have one
    'admin:index',  # Allow access to the Django admin without login redirect
]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_url = resolve(request.path_info).view_name
            if not request.user.is_authenticated and current_url not in EXEMPT_URLS:
                return redirect(settings.LOGIN_URL)
            response = self.get_response(request)
            return response
        except Resolver404:
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)
            raise
