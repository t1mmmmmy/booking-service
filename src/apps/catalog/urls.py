from django.urls import path

from apps.catalog import views
from apps.catalog.views import RoomViewSet

urlpatterns = [
    path("ping/", views.ping, name="ping"),
    path("rooms/list", RoomViewSet.as_view({"get": "list"})),
    path("rooms/create", RoomViewSet.as_view({"post": "create"})),
    path("rooms/delete/<int:pk>", RoomViewSet.as_view({"delete": "destroy"})),
    path("bookings/list", views.BookingViewSet.as_view({"get": "list"})),
    path("bookings/create", views.BookingViewSet.as_view({"post": "create"})),
    path("bookings/delete/<int:pk>", views.BookingViewSet.as_view({"delete": "destroy"})),
]
