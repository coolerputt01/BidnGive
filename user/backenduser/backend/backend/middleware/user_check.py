from django.http import JsonResponse

class DisableInactiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and getattr(request.user, 'is_disabled', False):
            return JsonResponse({'error': 'Account disabled. Please reactivate.'}, status=403)
        return self.get_response(request)
