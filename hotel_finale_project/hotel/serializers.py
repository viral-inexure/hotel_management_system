from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Profile, Hotel, HotelRoomType, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'mobile_number', 'address', 'email',
                  'password', 'is_superuser', 'is_staff'
                  ]

    def create(self, validated_data):
        user_detail = {
            'username': validated_data['username'],
            'password': make_password(validated_data['password']),
            'is_staff': validated_data['is_staff'],
            'is_superuser': validated_data['is_superuser']
        }
        Profile.objects.create(**user_detail)
        return validated_data


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'contact', 'address', 'zip', 'city', 'country']


class HotelRoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoomType
        fields = ['id', 'hotel', 'room_no', 'room_type', 'rate', 'is_available', 'person_cap']


class HotelReservation(serializers.ModelSerializer):
    user = UserSerializer
    room = HotelRoomTypeSerializer
    hotel = HotelSerializer

    class Meta:
        model = Reservation
        fields = ['id', 'username', 'room', 'no_of_guests', 'hotel', 'check_in',
                  'check_out_done', 'check_out', 'payment_type', 'payment_date',
                  'charge']

