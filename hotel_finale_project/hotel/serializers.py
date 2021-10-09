from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Profile, Hotel, HotelRoomType, Reservation


class UserSerializer(serializers.ModelSerializer):
    """user profile serializer nad validations """
    class Meta:
        model = Profile
        fields = ['username', 'mobile_number', 'address', 'email',
                  'password', 'is_superuser', 'is_staff'
                  ]
        extra_kwargs = {
            'username': {'required': True},
            'mobile_number': {'required': True},
            'address': {'required': True},
            'password': {'required': True},
            'email': {'required': True},
        }

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
    """hotel serializer"""
    class Meta:
        model = Hotel
        fields = ['name', 'contact', 'address', 'zip', 'city', 'country']
        extra_kwargs = {
            'name': {'required': True},
            'contact': {'required': True},
            'address': {'required': True},
            'zip': {'required': True},
            'city': {'required': True},
            'country': {'required': True},
        }


class HotelRoomTypeSerializer(serializers.ModelSerializer):
    """ hotel room type serializer"""
    class Meta:
        model = HotelRoomType
        fields = ['hotel', 'room_no', 'room_type', 'rate', 'is_available', 'person_cap']

        extra_kwargs = {
            'hotel': {'required': True},
            'room_no': {'required': True},
            'room_type': {'required': True},
            'rate': {'required': True},
            'is_available': {'required': True},
            'person_cap': {'required': True},
        }


class HotelReservation(serializers.ModelSerializer):
    """hotel reservation """
    user = UserSerializer
    room = HotelRoomTypeSerializer
    hotel = HotelSerializer

    class Meta:
        model = Reservation
        fields = ['username', 'room', 'no_of_guests', 'hotel', 'check_in',
                  'check_out_done', 'check_out', 'payment_type', 'payment_date',
                  'charge']

        extra_kwargs = {
            'username': {'required': True},
            'room': {'required': True},
            'no_of_guests': {'required': True},
            'hotel': {'required': True},
            'check_in': {'required': True},
        }
