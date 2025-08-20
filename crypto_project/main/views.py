from django.http import Http404
from django.shortcuts import render

from crypto_project.customer.models import Customer


def homepage(request):
    try:
        customer = request.user.customer
    except AttributeError:
        customer = None
    return render(request, "homepage.html", {'customer': customer})
