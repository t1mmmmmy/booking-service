from django.http.request import HttpRequest
from django.http.response import JsonResponse

# Create your views here.


def ping(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": 200})
