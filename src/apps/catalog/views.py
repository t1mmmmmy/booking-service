from typing import Any

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import filters, serializers, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.catalog.models import Booking, Room
from apps.catalog.serializers import BookingSerializer, RoomSerializer


# Create your views here.
class RoomViewSet(viewsets.ModelViewSet[Room]):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "added_at"]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().create(request, *args, **kwargs)
        response.data = {"room_id": response.data["id"]}
        return response


class BookingViewSet(viewsets.ModelViewSet[Booking]):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        room_id = self.request.query_params.get("room_id")
        if room_id is not None:
            room_id = serializers.IntegerField(min_value=1).run_validation(room_id)
            queryset = queryset.filter(room_id=room_id)
        return queryset

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().create(request, *args, **kwargs)
        response.data = {"booking_id": response.data["id"]}
        return response


def ping(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": 200})
