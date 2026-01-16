from django.http import JsonResponse
from django_ratelimit.exceptions import Ratelimited


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """
        This method is called when a view raises an exception.
        """
        if isinstance(exception, Ratelimited):
            # Return a JSON response for APIs
            return JsonResponse(
                {"error": "Too many requests", "message": "Please try again later."},
                status=429
            )
        return None
