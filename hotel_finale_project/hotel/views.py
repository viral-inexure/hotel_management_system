from datetime import datetime
from rest_framework.permissions import AllowAny
from .models import Profile, Hotel, HotelRoomType, Reservation
from .serializers import UserSerializer, HotelSerializer, HotelRoomTypeSerializer, HotelReservation, RegisterSerializer
from rest_framework import viewsets, permissions, generics
from .permissions import IsStaff
from rest_framework.response import Response


class UserView(viewsets.ModelViewSet):
    """ user view and CRUD operation for userdata and also permissions for different user"""
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return (AllowAny() if self.request.method in permissions.SAFE_METHODS else IsStaff()),


class RegisterView(generics.CreateAPIView):
    """user registration """
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class HotelView(viewsets.ModelViewSet):
    """ hotel view and CRUD operation for hotel data and also permissions for different user"""

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        return (AllowAny() if self.request.method in permissions.SAFE_METHODS else IsStaff()),


class HotelRoomsTypeAvailable(viewsets.ModelViewSet):
    """ hotel room type where check room is available or not if not create room or update room"""

    queryset = HotelRoomType.objects.all()
    serializer_class = HotelRoomTypeSerializer

    def get_permissions(self):
        return (AllowAny() if self.request.method in permissions.SAFE_METHODS else IsStaff()),


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
    """ this class  used for check user bill amount by date"""
    lookup_url_kwarg = ['start_date', 'end_date']

    def get(self, request, *args, **kwargs):
        try:
            start_date = request.GET.get(self.lookup_url_kwarg[0])
            end_date = request.GET.get(self.lookup_url_kwarg[1])
            reservation_obj = Reservation.objects.filter(username=request.user).filter(check_out_done=False).all()
            for reservation_user in reservation_obj:
                res_start_date = reservation_user.check_in
                res_end_date = reservation_user.check_out
                user_start_date_input_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                user_end_date_input_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                rate_hotel = reservation_user.room.rate
                if not reservation_user.check_out_done:
                    if (res_start_date.date() <= user_start_date_input_date <= res_end_date.date()) \
                            and (res_end_date.date() >= user_end_date_input_date >= res_start_date.date()):
                        difference_date = user_end_date_input_date - user_start_date_input_date
                        if user_end_date_input_date == user_start_date_input_date:
                            amount = 1 * rate_hotel
                        else:
                            amount = difference_date.days * rate_hotel
                        amount_dict = {
                            'reservation_data': reservation_user.id,
                            'start_date': user_start_date_input_date,
                            'end_date': user_end_date_input_date,
                            'amount': amount,
                        }
                        return Response(amount_dict)
                    else:
                        return Response('you have enter wrong date')
                else:
                    return Response('already check out')
        except (AttributeError, ValueError, TypeError):
            return Response("did not enter date or you don't have reservation")
