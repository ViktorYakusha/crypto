from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def registration(request):
    if request.method == 'POST':
        print(request.POST)
        response_data = {'status': 'success'}
        return JsonResponse(response_data)
    return JsonResponse({'message': 'Invalid request method'}, status=400)