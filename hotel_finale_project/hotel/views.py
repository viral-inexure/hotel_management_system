from datetime import datetime
from .models import Profile, Hotel, HotelRoomType, Reservation
from .serializers import UserSerializer, HotelSerializer, HotelRoomTypeSerializer, HotelReservation
from rest_framework import viewsets, permissions, generics
from .permissions import IsStaff
from rest_framework.response import Response


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


class UserBillCheck(generics.ListAPIView):

    lookup_url_kwarg = ['reservation', 'start_date', 'end_date']

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get(self.lookup_url_kwarg[1])
        end_date = request.GET.get(self.lookup_url_kwarg[2])
        reservation_obj = Reservation.objects.filter(username=request.user).first()
        res_start_date = reservation_obj.check_in
        res_end_date = reservation_obj.check_out
        user_start_date_input_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        user_end_date_input_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        rate_hotel = reservation_obj.room.rate
        if (res_start_date.date() <= user_start_date_input_date) \
                and (res_end_date.date() >= user_end_date_input_date):
            difference_date = user_end_date_input_date - user_start_date_input_date
            amount = difference_date.days * rate_hotel
            amount_dict = {
                'reservation_data': reservation_obj.id,
                'start_date': user_start_date_input_date,
                'end_date': user_end_date_input_date,
                'amount': amount,
            }
            return Response(amount_dict)
        else:
            return Response('you have enter wrong date')

        # practice_url =  'http://127.0.0.1:8000/practice/?reservation=4&start_date=2021-10-12&end_date=2021-10-15'

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = self.queryset.all()
        else:
            user = self.request.user
            a = Reservation.objects.filter(username=user).first()
            queryset = self.queryset.filter(reservation=a).all()
        return queryset
