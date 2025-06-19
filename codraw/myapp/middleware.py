class SlidingTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        new_token = getattr(request, 'jwt', None)
        if new_token:
            response.set_cookie(
                'jwt',
                new_token,
                httponly=True,
                secure=True,
                max_age=900,  # 5 minutes
            )
        return response