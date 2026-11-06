from typing import Any

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from loguru import logger
from rest_framework import filters, serializers, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.catalog.logging_setup import setup_logging
from apps.catalog.models import Booking, Room
from apps.catalog.serializers import BookingSerializer, RoomSerializer

setup_logging()


# Create your views here.
class RoomViewSet(viewsets.ModelViewSet[Room]):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "added_at"]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().create(request, *args, **kwargs)
        response.data = {"room_id": response.data["id"]}
        logger.info("Создан номер room_id: {}", response.data["room_id"])
        return response

    def perform_destroy(self, instance: Room) -> None:
        room_id = instance.pk
        super().perform_destroy(instance)
        logger.info("Комната удалена room_id: {}", room_id)


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
        logger.info(
            "Создана бронь booking_id: {}, room_id: {}",
            response.data["id"],
            response.data["room"],
        )
        response.data = {"booking_id": response.data["id"]}
        return response

    def perform_destroy(self, instance: Booking) -> None:
        booking_id = instance.pk
        room_id = instance.room_id
        super().perform_destroy(instance)
        logger.info("Бронь удалена booking_id: {}, room_id: {}", booking_id, room_id)


def ping(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": 200})
