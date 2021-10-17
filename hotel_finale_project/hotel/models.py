from django.db import models
from django.contrib.auth.models import AbstractUser
from constants import (
    SINGLE, HALL, KING,
    QUEEN, DOUBLE, HOTEL, ROOM_NO, CASH, CREDIT_DEBIT_CARD, CHECK, NET_BANKING
)


class Profile(AbstractUser):
    """ User detail or registration data table"""
    mobile_number = models.IntegerField()
    address = models.CharField(max_length=250)
    email = models.EmailField(max_length=150)

    def __str__(self):
        return str(self.username)


class Hotel(models.Model):
    """hotel database table"""
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=10)
    address = models.TextField(max_length=200)
    zip = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HotelRoomType(models.Model):
    """hotel room type data table """
    ROOMS_TYPE = (
        (SINGLE, 1),
        (DOUBLE, 2),
        (KING, 3),
        (QUEEN, 4),
        (HALL, 5)
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_no = models.IntegerField(null=True, blank=True)
    room_type = models.CharField(max_length=100, choices=ROOMS_TYPE)
    rate = models.FloatField()
    is_available = models.BooleanField(default=True)
    person_cap = models.IntegerField()

    class Meta:
        unique_together = (HOTEL, ROOM_NO)

    def __str__(self):
        return str(f'{self.hotel.name} of {self.room_no}')


class Reservation(models.Model):
    """user reservation table"""
    PAYMENT_METHOD = (
        (CASH, 1),
        (NET_BANKING, 2),
        (CHECK, 3),
        (CREDIT_DEBIT_CARD, 4)
    )
    room = models.ForeignKey(HotelRoomType, on_delete=models.CASCADE)
    username = models.ForeignKey(Profile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    check_out_done = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_METHOD)
    no_of_guests = models.IntegerField()
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username.username

    def charge(self):
        if self.check_out_done:
            if self.check_in == self.check_out:
                return self.room.rate
            else:
                time_delta = self.check_in - self.check_out
                total_time = time_delta.days
                total_cost = total_time * self.room.rate
                return abs(total_cost)
        else:
            return 'payment count is pending'
