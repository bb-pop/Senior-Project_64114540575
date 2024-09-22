from django.shortcuts import redirect
from django.urls import reverse

class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path == reverse('admin:index'):
            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                return redirect('/index-admin/')
        return None
