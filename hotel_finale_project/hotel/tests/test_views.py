from django.test import TestCase, Client
from django.urls import reverse
from ..models import (Profile, Hotel, Reservation, HotelRoomType)


class TestView(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = Profile.objects.create_superuser(username="admin",
                                                     email="viralpy1@gmail.com",
                                                     mobile_number="9228110541",
                                                     password="123"
                                                     )
        self.user.save()
        self.client.login(username=self.user.username, password=self.user.password)
        self.hotel = Hotel.objects.create(
            name='nikoliyan',
            contact='989654',
            address='nikol',
            zip='985632',
            city='ahmedabad',
            country='india',
        )

        self.hotel_room = HotelRoomType.objects.create(
            hotel=self.hotel,
            room_no='102',
            room_type='single',
            rate=1500,
            is_available=1,
            person_cap=2
        )

        self.reservation = Reservation.objects.create(
            room=self.hotel_room,
            username=self.user,
            hotel=self.hotel,
            check_in='2021-02-20 12:00',
            check_out='2021-02-20 12:00',
            check_out_done=True,
            payment_type=1,
            no_of_guests=2,
        )

    def test_get_hotel_list(self):
        self.client.login(username=self.user.username, password=self.user.password)
        res = self.client.get(reverse('hotel:hotel_data-detail', args=[1]), )
        self.assertEqual(res.status_code, 200)

    def test_hotel_view(self):
        self.data = {
            'name': 'nikoliyan',
            'contact': '989654',
            'address': 'nikol',
            'zip': '985632',
            'city': 'ahmedabad',
            'country': 'india'
        }
        res = self.client.post('/hotel', json=self.data)
        self.assertEqual(res.status_code, 301)

    def test_hotel_update_view(self):
        self.data = {
            'name': 'taj',
            'contact': '1234',
            'address': 'sola',
            'zip': '985632',
            'city': 'ahmedabad',
            'country': 'india'
        }
        res = self.client.put('/hotel/1', json=self.data)
        self.assertEqual(res.status_code, 301)

    def test_hotel_delete_view(self):
        res = self.client.delete('/hotel/1')
        self.assertEqual(res.status_code, 301)

    def test_user_view(self):
        data = {
            "username": "admin",
            "mobile_number": 123,
            "address": "",
            "email": "viral@123.gmail.com",
            "password": "pbkdf2_sha256$260000$IUQX4vjlaS8ftBziFqNk6L$px0NAx5IsYcjPHjlwODznXDOXuAwFDol2qSV5jhQsq8=",
            "is_superuser": True,
            "is_staff": True
        }
        res = self.client.post('/user', json=data)
        self.assertEqual(res.status_code, 301)

    def test_user_update(self):
        self.client.login(username=self.user.username, password=self.user.password)
        data = {
            "username": "admin",
            "mobile_number": 123798887878,
            "address": "nikol",
            "email": "viral@123.gmail.com",
            "password": "pbkdf2_sha256$260000$IUQX4vjlaS8ftBziFqNk6L$px0NAx5IsYcjPHjlwODznXDOXuAwFDol2qSV5jhQsq8=",
            "is_superuser": True,
            "is_staff": True
        }

        res = self.client.put('/user/1', json=data)
        self.assertEqual(res.status_code, 301)

    def test_user_delete_view(self):
        res = self.client.delete('/user/1')
        self.assertEqual(res.status_code, 301)

    def test_hotel_room_type_view(self):
        self.client.login(username=self.user.username, password=self.user.password)
        res = self.client.get(reverse('hotel:hotel_room_data-list'))
        self.assertEqual(res.status_code, 200)

    def test_hotel_room_type_view_update(self):
        data = {'hotel': self.hotel,
                'room_no': '102',
                'room_type': 'single',
                'rate': 1500,
                'is_available': 1,
                'person_cap': 2}
        self.client.login(username=self.user.username, password=self.user.password)
        res = self.client.put('/hotel_room/1', json=data)
        self.assertEqual(res.status_code, 301)

    def test_hotel_room_type_view_delete(self):
        self.client.login(username=self.user.username, password=self.user.password)
        res = self.client.delete('/hotel_room/1')
        self.assertEqual(res.status_code, 301)

    def test_hotel_reservation_update_view(self):
        data = {
            'room': self.hotel_room,
            'username': self.user,
            'hotel': self.hotel,
            'check_in': '2021-02-20 12:00',
            'check_out': '2021-03-22 1:00',
            'check_out_done': True,
            'payment_type': 1,
            'no_of_guests': 2,
            'payment_date': '2021-03-23 12:00'
        }
        self.client.login(username=self.user.username, password=self.user.password)
        res = self.client.put('/hotel_room/1', json=data)
        self.assertEqual(res.status_code, 301)

    def test_hotel_reservation_delete_view(self):
        self.client.login(username=self.user.username, password=self.user.password)
        res = self.client.delete('/hotel_reservation/1')
        self.assertEqual(res.status_code, 301)