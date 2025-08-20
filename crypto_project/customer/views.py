from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from authtools.forms import UserCreationForm

from .forms import CustomerRegistrationForm


@csrf_protect
def customer_registration(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerRegistrationForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            response_data = {'status': 'success'}
            return JsonResponse(response_data)

        else:
            return JsonResponse({'status': 'error', 'user_form': user_form.errors, 'customer_form': customer_form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_protect
def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                response_data = {'status': 'success'}
                return JsonResponse(response_data, status=200)
            else:
                response_data = {'status': 'error', 'error': 'Email or password is incorrect'}
            return JsonResponse(response_data, status=400)

        else:
            response_data = {'status': 'error', 'error': 'Enter email and password'}
            return JsonResponse(response_data, status=400)
    response_data = {'status': 'error', 'error': 'Invalid request method.'}
    return JsonResponse(response_data, status=400)

@login_required
def customer_logout(request):
    logout(request)
    return redirect('/')

@login_required
def customer_profile(request):
    customer = request.user.customer
    if customer is None:
        raise Http404("Item not found")
    return render(request, 'profile.html', {'customer': customer})

@login_required
def customer_profile_account(request):
    customer = request.user.customer
    if customer is None:
        raise Http404("Item not found")
    return render(request, 'account.html', {'customer': customer})

@login_required
def customer_profile_bills(request):
    customer = request.user.customer
    if customer is None:
        raise Http404("Item not found")
    return render(request, 'bills.html', {'customer': customer})

@login_required
def customer_profile_settings(request):
    customer = request.user.customer
    if customer is None:
        raise Http404("Item not found")
    return render(request, 'settings.html', {'customer': customer})