from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from ..models import Customer


class CustomerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/profile'):
            try:
                customer = request.user.customer
            except Customer.DoesNotExist:
                logout(request)
                return HttpResponseRedirect(reverse('homepage'))

            request.customer = customer
        response = self.get_response(request)
        return response