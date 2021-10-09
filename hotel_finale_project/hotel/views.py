from .models import Profile, Hotel, HotelRoomType, Reservation
from .serializers import UserSerializer, HotelSerializer, HotelRoomTypeSerializer, HotelReservation
from rest_framework import viewsets, permissions
from .permissions import IsStaff


class UserView(viewsets.ModelViewSet):
    """ user view and CRUD operation for userdata and also permissions for different user"""
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'POST' else IsStaff()),


class HotelView(viewsets.ModelViewSet):
    """ hotel view and CRUD operation for hotel data and also permissions for different user"""

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'GET' else IsStaff()),


class HotelRoomsTypeAvailable(viewsets.ModelViewSet):
    """ hotel room type where check room is available or not if not create room or update room"""

    queryset = HotelRoomType.objects.all()
    serializer_class = HotelRoomTypeSerializer

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'GET' else IsStaff()),


class ReservationHotel(viewsets.ModelViewSet):
    """ reservation for user and select payment and also check out from the hotel"""
    queryset = Reservation.objects.all()
    serializer_class = HotelReservation

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = self.queryset.all()
        else:
            user = self.request.user
            queryset = self.queryset.filter(username=user).all()
        return queryset
