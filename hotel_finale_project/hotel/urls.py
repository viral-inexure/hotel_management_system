from django.urls import path, include
from rest_framework import routers
from .views import UserView, HotelView, HotelRoomsAvailable, ReservationHotel

router = routers.DefaultRouter()
router.register('user', UserView, basename='user_data')
router.register('hotel', HotelView, basename='hotel_data')
router.register('hotel_room', HotelRoomsAvailable, basename='hotel_room_data')
router.register('hotel_reservation', ReservationHotel, basename='hotel_reservation')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_auth.urls'))
    # path('api/rest-auth/', include('rest_auth.urls')),
]
