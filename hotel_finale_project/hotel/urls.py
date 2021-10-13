from django.urls import path, include
from rest_framework import routers
from .views import UserView, HotelView, HotelRoomsTypeAvailable, ReservationHotel, UserBillCheck

app_name = 'hotel'
router = routers.DefaultRouter()
router.register('user', UserView, basename='user_data')
router.register('hotel', HotelView, basename='hotel_data')
router.register('hotel_room', HotelRoomsTypeAvailable, basename='hotel_room_data')
router.register('hotel_reservation', ReservationHotel, basename='hotel_reservations')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_auth.urls')),
    path('UserBillCheck/', UserBillCheck.as_view(), name='Practice'),
    # 'http://127.0.0.1:8000/practice/?reservation=4&start_date=2021-10-12&end_date=2021-10-15'

]
