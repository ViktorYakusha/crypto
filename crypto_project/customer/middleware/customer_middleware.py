from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from ..models import Customer


class CustomerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            customer = request.user.customer
            request.customer = customer
        except (Customer.DoesNotExist, AttributeError):
            if request.path.startswith('/profile'):
                logout(request)
                return HttpResponseRedirect(reverse('homepage'))

        response = self.get_response(request)
        return response