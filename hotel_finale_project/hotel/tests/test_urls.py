from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestUrls(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_urls_of_user_login(self):
        url = '/api-auth/login'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)

    def test_urls_of_user(self):
        url = '/user'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)

    def test_urls_of_hotel(self):
        url = '/hotel/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_urls_of_hotel_room(self):
        url = '/hotel_room/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_urls_of_hotel_reservation(self):
        url = '/hotel_reservation'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)

    def test_check_user_amount_url(self):
        url = '/UserBillCheck'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
