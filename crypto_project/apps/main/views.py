from django.http import Http404
from django.shortcuts import render


def homepage(request):
    return render(request, "homepage.html")
