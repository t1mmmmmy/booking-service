from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.catalog.models import Room


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def rooms() -> list[Room]:
    return [
        Room.objects.create(
            description="Room 1",
            price=Decimal("400.00"),
        ),
        Room.objects.create(
            description="Room 2",
            price=Decimal("500.00"),
        ),
        Room.objects.create(
            description="Room 3",
            price=Decimal("100.00"),
        ),
    ]
