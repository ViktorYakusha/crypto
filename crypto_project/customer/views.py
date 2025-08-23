from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from authtools.forms import UserCreationForm
from django.utils import timezone
from datetime import timedelta

from .forms import CustomerRegistrationForm, BetForm


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
def customer_create_bet(request):
    if request.method == 'POST' and request.user.customer:
        bet_form = BetForm(request.POST)
        summa = float(request.POST['summa'])
        duration = int(request.POST['duration'])

        if bet_form.is_valid() and request.user.customer.balance >= summa and duration in [1, 5, 15, 30, 60, 240]:
            bet = bet_form.save(commit=False)
            bet.customer = request.user.customer
            bet.close_date = timezone.now() + timedelta(minutes=duration)

            # add profit
            profit = round((summa * 0.81), 2)
            if not request.user.customer.trading:
                profit = profit * -1
            bet.profit = profit
            bet.save()

            # update customer balance
            request.user.customer.balance = round(request.user.customer.balance - summa, 2)
            request.user.customer.save()
            response_data = {'status': 'success'}
            return JsonResponse(response_data)

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


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
    return render(request, 'profile.html')

@login_required
def customer_profile_account(request):
    return render(request, 'account.html')

@login_required
def customer_profile_bills(request):
    return render(request, 'bills.html')

@login_required
def customer_profile_settings(request):
    return render(request, 'settings.html')