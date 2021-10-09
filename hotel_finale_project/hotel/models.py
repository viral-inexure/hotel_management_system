import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class Profile(AbstractUser):
    mobile_number = models.IntegerField(default=123)
    address = models.CharField(max_length=250)
    email = models.EmailField(max_length=150)

    def __str__(self):
        return str(self.username)


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=10)
    address = models.TextField(max_length=200)
    zip = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HotelRoomType(models.Model):
    ROOMS_TYPE = (
        (1, 'single'),
        (2, 'double'),
        (3, 'king'),
        (4, 'queen'),
        (5, 'hall')
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_no = models.IntegerField(null=True, blank=True)
    room_type = models.CharField(max_length=100, choices=ROOMS_TYPE)
    rate = models.FloatField()
    is_available = models.BooleanField(default=True)
    person_cap = models.IntegerField(default=1)

    class Meta:
        unique_together = ('hotel', 'room_no')

    def __str__(self):
        return str(f'{self.hotel.name} of {self.room_no}')


class Reservation(models.Model):
    PAYMENT_METHOD = (
        (1, 'CASH'),
        (2, 'NET BANKING'),
        (3, 'CHECK'),
        (4, 'CREDIT/DEBIT CARD')
    )
    room = models.ForeignKey(HotelRoomType, on_delete=models.CASCADE)
    username = models.ForeignKey(Profile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))
    check_out_done = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_METHOD)
    no_of_guests = models.IntegerField(default=1)
    payment_date = models.DateTimeField(auto_now_add=True)

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


@receiver(post_save, sender=Reservation)
def Room_available(sender, instance, created, **kwargs):
    room = instance.room
    if created:
        room.is_available = False
    room.save()

    if instance.check_out_done:
        room.is_available = True

    room.save()
