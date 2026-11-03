from decimal import Decimal
from typing import Any

from rest_framework import serializers

from apps.catalog.models import Booking, Room


class RoomSerializer(serializers.ModelSerializer[Room]):
    class Meta:
        model = Room
        fields = "__all__"

    def validate_price(self, price: Decimal) -> Decimal:
        if price <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        return price


class BookingSerializer(serializers.ModelSerializer[Booking]):
    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if data["date_start"] >= data["date_end"]:
            raise serializers.ValidationError(
                "Дата начала должна быть раньше даты конца бронирования"
            )
        return data
