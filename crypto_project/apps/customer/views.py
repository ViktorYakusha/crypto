from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from .forms import CustomerRegistrationForm


@csrf_protect
def registration(request):
    if request.method == 'POST':
        customer_form = CustomerRegistrationForm(request.POST)
        if customer_form.is_valid():
            new_customer = customer_form.save(commit=False)
            new_customer.set_password(customer_form.cleaned_data['password'])
            new_customer.save()
            response_data = {'status': 'success'}
            return JsonResponse(response_data)
    return JsonResponse({'message': 'Invalid request method'}, status=400)