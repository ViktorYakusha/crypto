class CustomerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            customer = request.user.customer
        except AttributeError:
            customer = None

        request.customer = customer
        response = self.get_response(request)
        return response