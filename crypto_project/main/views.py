from django.http import Http404
from django.shortcuts import render

from crypto_project.customer.models import Customer


def homepage(request):
    return render(request, "homepage.html", {})
