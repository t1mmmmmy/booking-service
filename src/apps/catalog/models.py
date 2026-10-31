# Create your models here.
from django.db import models
from django.db.models.query_utils import Q


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=19, null=False)
    description = models.TextField(null=False)
    added_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(price__gt=0), name="room_price_must_be_positive"),
        ]


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ["date_start"]
        constraints = [
            models.CheckConstraint(
                condition=Q(date_start__lt=models.F("date_end")),
                name="booking_date_start_earlier_than_date_end",
            ),
        ]
