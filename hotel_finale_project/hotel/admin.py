from django.contrib import admin
from .models import Profile, Hotel, HotelRoomType, Reservation

admin.site.register(Hotel)


class Profile_admin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_superuser', 'is_staff')


class Hotel_room_admin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'rate', 'is_available')


class Reservation_admin(admin.ModelAdmin):
    list_display = ('username', 'hotel', 'room', 'reservation_date')


admin.site.register(Profile, Profile_admin)
admin.site.register(HotelRoomType, Hotel_room_admin)
admin.site.register(Reservation, Reservation_admin)
