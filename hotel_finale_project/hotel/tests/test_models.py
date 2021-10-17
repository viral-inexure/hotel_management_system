from django.test import TestCase
from ..models import Profile, Hotel, Reservation, HotelRoomType
from datetime import datetime


class TestModel(TestCase):

    def setUp(self):
        self.user = Profile.objects.create_user(username="admin",
                                                email="viralpy1@gmail.com",
                                                mobile_number="9228110541",
                                                password="123"
                                                )
        self.hotel = Hotel.objects.create(
            name='nikoliyan',
            contact='989654',
            address='nikol',
            zip='985632',
            city='ahmedabad',
            country='india'
        )

        self.hotel_room = HotelRoomType.objects.create(
            hotel=self.hotel,
            room_no='102',
            room_type='single',
            rate=1500,
            is_available=1,
            person_cap=2
        )

    def tearDown(self):
        self.user.delete()

    def test_user_model(self):
        user = Profile.objects.create(username="viren", email="viren@gmail.com",
                                      mobile_number="9228110541", password="123")
        self.assertEqual(str(user), user.username)

    def test_hotel_model(self):
        self.assertEqual(str(self.hotel), self.hotel.name)

    def test_hotel_room_model(self):
        self.assertEqual(str(self.hotel_room), f'{self.hotel.name} of {self.hotel_room.room_no}')

    def test_hotel_reservation_model(self):
        reservation = Reservation.objects.create(
            room=self.hotel_room,
            username=self.user,
            hotel=self.hotel,
            check_in=datetime.now(),
            check_out=datetime.now(),
            check_out_done=True,
            payment_type=1,
            no_of_guests=2,
        )
        self.assertEqual(str(reservation), self.user.username)
