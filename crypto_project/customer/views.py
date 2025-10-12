import json
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from celery import shared_task
from authtools.forms import UserCreationForm
from django.utils import timezone
from datetime import timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import CustomerRegistrationForm, BetForm, CustomPasswordChangeForm
from .models import Bet, BankCard, CryptoWallet


@csrf_protect
def customer_registration(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
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
        try:
            summa = float(request.POST['summa'])
        except ValueError as e:
            summa = 0
        duration = int(request.POST['duration'])

        if bet_form.is_valid() and request.user.customer.balance >= summa and  summa > 0 and duration in [1, 5, 15, 30, 60, 240]:
            bet = bet_form.save(commit=False)
            bet.customer = request.user.customer
            bet.close_date = timezone.now() + timedelta(minutes=duration)

            # add profit
            profit = round((summa * 0.81), 2)
            if not request.user.customer.trading:
                profit = profit * -1
            bet.profit = profit
            bet.save()
            # celery close task
            close_bet.apply_async((bet.id,), eta=bet.close_date)
            # ws event
            channel_layer = get_channel_layer()
            group_name = f'user_{request.user.id}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_personal_message',
                    'message': 'open_bet'
                }
            )

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
        long = request.POST.get('long')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                if long:
                    request.session.set_expiry(60 * 60 * 24)
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
    closed_bets = Bet.objects.filter(customer=customer, entry__gt=0).order_by('-open_date')
    opened_bets = Bet.objects.filter(customer=customer, entry=0).order_by('-open_date')
    return render(request, 'profile.html', {'closed_bets': closed_bets, 'opened_bets': opened_bets})

@login_required
def customer_profile_account(request):
    return render(request, 'account.html')

@login_required
def customer_profile_bills(request):
    return render(request, 'bills.html')

@login_required
def customer_profile_settings(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')  # Redirect to a success page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'settings.html', {'form': form})

@login_required
@csrf_protect
def customer_load_payments(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        bank_cards = BankCard.objects.all()
        bank_cards_obs = list(
            map(lambda item: {'name': item.name, 'bank_name': item.bank_name, 'card_number': item.card_number},
                bank_cards))
        crypto_wallets = CryptoWallet.objects.filter(is_active=True)
        crypto_wallets_obs = list(map(lambda item: {'network': item.network, 'wallet': item.wallet, 'label': item.get_network_display()}, crypto_wallets))
        return JsonResponse({'status': 'success', 'bank_cards': bank_cards_obs, 'crypto': crypto_wallets_obs}, safe=False)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@csrf_protect
def customer_load_open_bets(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        customer = request.user.customer
        opened_bets = Bet.objects.filter(customer=customer, entry=0).order_by('close_date')
        balance = request.user.customer.balance
        json_opened_bets = serializers.serialize("json", opened_bets, fields=['quotation', 'summa', 'open_date', 'close_date', 'entry', 'profit'])
        return JsonResponse({'status': 'success', 'bets': json_opened_bets, 'balance': balance}, safe=False)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@csrf_protect
def customer_load_close_bets(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        customer = request.user.customer
        closed_bets = Bet.objects.filter(customer=customer, entry__gt=0).order_by('-close_date')
        json_closed_bets = serializers.serialize("json", closed_bets, fields=['quotation', 'summa', 'open_date', 'close_date', 'entry', 'profit'])
        return JsonResponse({'status': 'success', 'bets': json_closed_bets}, safe=False)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@shared_task
def close_bet(bet_id):
    bet = Bet.objects.get(id=bet_id)
    bet.entry = round(bet.summa + bet.profit, 2)
    bet.save()
    bet.customer.balance = round(bet.customer.balance + bet.entry, 2)
    bet.customer.save()
    channel_layer = get_channel_layer()
    group_name = f'user_{bet.customer.user.id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_personal_message',
            'message': 'close_bet'
        }
    )
    print('Closing bet---------------- {}'.format(bet_id))