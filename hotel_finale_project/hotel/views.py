from django.shortcuts import render
from .models import Profile, Hotel, HotelRoomType, Reservation
from .serializers import UserSerializer, HotelSerializer, HotelRoomTypeSerializer, HotelReservation
from rest_framework import viewsets, permissions
from .permissions import IsHeadOrReadOnly, IsStaff


class UserView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'POST' else IsStaff()),


class HotelView(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'GET' else IsStaff()),


class HotelRoomsAvailable(viewsets.ModelViewSet):
    queryset = HotelRoomType.objects.all()
    serializer_class = HotelRoomTypeSerializer

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'GET' else IsStaff()),


class ReservationHotel(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = HotelReservation

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = self.queryset.all()
        else:
            user = self.request.user
            queryset = self.queryset.filter(username=user).all()
        return queryset
