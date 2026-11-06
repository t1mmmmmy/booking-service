import pytest
from rest_framework.test import APIClient

from apps.catalog.models import Booking, Room


@pytest.mark.django_db
def test_create_booking(client: APIClient, rooms: list[Room]) -> None:
    response = client.post(
        "/bookings/create",
        data={
            "date_start": "2020-04-01",
            "date_end": "2020-05-01",
            "room": rooms[0].pk,
        },
        format="json",
    )
    body = response.json()
    assert response.status_code == 201
    assert "booking_id" in body


@pytest.mark.django_db
@pytest.mark.parametrize(
    "date_start, date_end",
    [
        ("", "2025-01-01"),
        ("2020-04-01", ""),
        ("2020 05 01", "2020-05-01"),
        ("2020-05-01", "2020 05 02"),
        ("2020.05.01", "2020-05-01"),
        ("2020-05-01", "2020.05.02"),
    ],
)
def test_create_with_invalid_dates(
    client: APIClient, rooms: list[Room], date_start: str, date_end: str
) -> None:
    response = client.post(
        "/bookings/create",
        data={
            "date_start": date_start,
            "date_end": date_end,
            "room": rooms[0].pk,
        },
        format="json",
    )
    body = response.json()
    assert response.status_code == 400
    assert "date_start" in body or "date_end" in body


@pytest.mark.django_db
@pytest.mark.parametrize("room", ["9999", ""])
def test_create_with_invalid_rooms(client: APIClient, rooms: list[Room], room: str) -> None:
    response = client.post(
        "/bookings/create",
        data={
            "date_start": "2020-04-01",
            "date_end": "2020-05-01",
            "room": room,
        },
        format="json",
    )
    body = response.json()
    assert response.status_code == 400
    assert "room" in body


@pytest.mark.django_db
def test_delete_room_cascade_bookings(client: APIClient, rooms: list[Room]) -> None:
    booking_1 = Booking.objects.create(
        date_start="2020-04-01",
        date_end="2020-05-01",
        room=rooms[0],
    )
    booking_2 = Booking.objects.create(
        date_start="2020-05-01",
        date_end="2020-06-01",
        room=rooms[1],
    )
    booking_3 = Booking.objects.create(
        date_start="2020-06-01",
        date_end="2020-07-01",
        room=rooms[0],
    )
    delete = client.delete(
        f"/rooms/delete/{rooms[1].pk}",
    )
    assert delete.status_code == 204
    response = client.get(
        "/bookings/list",
    )
    returned_ids = [item["id"] for item in response.json()]
    assert booking_1.pk in returned_ids
    assert booking_2.pk not in returned_ids
    assert booking_3.pk in returned_ids


@pytest.mark.django_db
def test_delete_booking(client: APIClient, rooms: list[Room]) -> None:
    booking_1 = Booking.objects.create(
        date_start="2020-04-01",
        date_end="2020-05-01",
        room=rooms[0],
    )
    response = client.delete(
        f"/bookings/delete/{booking_1.pk}",
    )
    assert response.status_code == 204
