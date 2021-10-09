from django.contrib import admin
from .models import Profile, Hotel, HotelRoomType, Reservation

# Register your models here.

admin.site.register(Profile)
admin.site.register(Hotel)
admin.site.register(HotelRoomType)
admin.site.register(Reservation)
