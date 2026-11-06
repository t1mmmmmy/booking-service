from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.catalog.models import Room


def test_ping(client: APIClient) -> None:
    response = client.get("/ping/")

    assert response.status_code == 200
    assert response.json() == {"status": 200}


@pytest.mark.django_db
def test_create_room(client: APIClient) -> None:
    response = client.post(
        "/rooms/create",
        data={
            "description": "Room 1",
            "price": "199.99",
        },
        format="json",
    )
    body = response.json()
    room = Room.objects.get(pk=body["room_id"])
    assert response.status_code == 201
    assert "room_id" in body
    assert room.description == "Room 1"
    assert room.price == Decimal("199.99")


@pytest.mark.django_db
@pytest.mark.parametrize("price", ["0", "-1", "abc", "199.999", "199999999999999999.99"])
def test_create_room_invalid_price(client: APIClient, price: str) -> None:
    num_of_rooms = Room.objects.count()
    response = client.post(
        "/rooms/create",
        data={
            "description": "Test Room",
            "price": price,
        },
        format="json",
    )
    body = response.json()
    assert response.status_code == 400
    assert Room.objects.count() == num_of_rooms
    assert "price" in body


@pytest.mark.django_db
def test_create_room_without_description(client: APIClient) -> None:
    response = client.post(
        "/rooms/create",
        data={
            "description": "",
            "price": "199.99",
        },
        format="json",
    )
    body = response.json()
    assert response.status_code == 400
    assert "description" in body


@pytest.mark.django_db
def test_create_room_without_price(client: APIClient) -> None:
    response = client.post(
        "/rooms/create",
        data={
            "description": "Room 1",
            "price": "",
        },
        format="json",
    )
    body = response.json()
    assert response.status_code == 400
    assert "price" in body


@pytest.mark.django_db
def test_rooms_list(client: APIClient, rooms: list[Room]) -> None:
    response = client.get("/rooms/list")
    body = response.json()
    assert response.status_code == 200
    assert len(body) == len(rooms)
    for i in range(len(rooms)):
        assert rooms[i].pk == body[i]["id"]


@pytest.mark.django_db
@pytest.mark.parametrize("ordering", ["price", "-price", "added_at", "-added_at"])
def test_list_rooms_ordering(client: APIClient, rooms: list[Room], ordering: str) -> None:
    response = client.get(f"/rooms/list?ordering={ordering}")
    returned_ids = [item["id"] for item in response.json()]
    assert response.status_code == 200
    if ordering == "price":
        assert returned_ids == [
            rooms[2].pk,
            rooms[0].pk,
            rooms[1].pk,
        ]
    elif ordering == "-price":
        assert returned_ids == [
            rooms[1].pk,
            rooms[0].pk,
            rooms[2].pk,
        ]
    elif ordering == "added_at":
        assert returned_ids == [
            rooms[0].pk,
            rooms[1].pk,
            rooms[2].pk,
        ]
    elif ordering == "-added_at":
        assert returned_ids == [
            rooms[2].pk,
            rooms[1].pk,
            rooms[0].pk,
        ]


@pytest.mark.django_db
def test_delete_room(client: APIClient, rooms: list[Room]) -> None:
    response = client.delete(f"/rooms/delete/{rooms[0].pk}")
    assert response.status_code == 204
    new_response = client.get("/rooms/list")
    returned_ids = [item["id"] for item in new_response.json()]
    assert rooms[0].pk not in returned_ids


@pytest.mark.django_db
def test_delete_unknown_room(client: APIClient, rooms: list[Room]) -> None:
    response = client.delete("/rooms/delete/999")
    assert response.status_code == 404
