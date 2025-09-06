
from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# 5 req/min for anonymous, 10 req/min for authenticated users
@ratelimit(key='ip', rate='5/m', block=True)
def anonymous_view(request):
    return JsonResponse({"message": "Anonymous view OK"})

@ratelimit(key='ip', rate='10/m', block=True)
def login_view(request):
    return JsonResponse({"message": "Login allowed"})
