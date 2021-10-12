from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Profile, Hotel, HotelRoomType, Reservation
from constants import (USERNAME, MOBILE_NUMBER, ADDRESS, EMAIL, PASSWORD,
                       IS_SUPERUSER, IS_STAFF, REQUIRED,
                       NAME, CONTACT, ZIP, CITY, COUNTRY,
                       HOTEL, ROOM_NO, ROOM_TYPE, RATE, IS_AVAILABLE, PERSON_CAP,
                       ROOM, NO_OF_GUESTS, CHECK_IN, CHARGE, CHECK_OUT_DONE,
                       CHECK_OUT, PAYMENT_TYPE, PAYMENT_DATE
                       )


class UserSerializer(serializers.ModelSerializer):
    """user profile serializer nad validations """

    class Meta:
        model = Profile
        fields = [USERNAME, MOBILE_NUMBER, ADDRESS, EMAIL,
                  PASSWORD, IS_SUPERUSER, IS_STAFF
                  ]
        extra_kwargs = {
            USERNAME: {REQUIRED: True},
            MOBILE_NUMBER: {REQUIRED: True},
            ADDRESS: {REQUIRED: True},
            PASSWORD: {REQUIRED: True},
            EMAIL: {REQUIRED: True},
        }

    def create(self, validated_data):
        user_detail = {
            'username': validated_data[USERNAME],
            'password': make_password(validated_data[PASSWORD]),
            'mobile_number': validated_data[MOBILE_NUMBER],
            'is_staff': validated_data[IS_STAFF],
            'is_superuser': validated_data[IS_SUPERUSER]
        }
        Profile.objects.create(**user_detail)
        return validated_data


class HotelSerializer(serializers.ModelSerializer):
    """hotel serializer"""

    class Meta:
        model = Hotel
        fields = [NAME, CONTACT, ADDRESS, ZIP, CITY, COUNTRY]
        extra_kwargs = {
            'name': {REQUIRED: True},
            'contact': {REQUIRED: True},
            'address': {REQUIRED: True},
            'zip': {REQUIRED: True},
            'city': {REQUIRED: True},
            'country': {REQUIRED: True},
        }


class HotelRoomTypeSerializer(serializers.ModelSerializer):
    """ hotel room type serializer"""

    class Meta:
        model = HotelRoomType
        fields = [HOTEL, ROOM_NO, ROOM_TYPE, RATE, IS_AVAILABLE, PERSON_CAP]

        extra_kwargs = {
            'hotel': {REQUIRED: True},
            'room_no': {REQUIRED: True},
            'room_type': {REQUIRED: True},
            'rate': {REQUIRED: True},
            'is_available': {REQUIRED: True},
            'person_cap': {REQUIRED: True},
        }


class HotelReservation(serializers.ModelSerializer):
    """hotel reservation """
    username = serializers.PrimaryKeyRelatedField(read_only=True)
    room = HotelRoomTypeSerializer
    hotel = HotelSerializer

    class Meta:
        model = Reservation
        fields = [USERNAME, HOTEL, NO_OF_GUESTS, ROOM, CHECK_IN,
                  CHECK_OUT_DONE, CHECK_OUT, PAYMENT_TYPE, PAYMENT_DATE]

        read_only_fields = [USERNAME, CHARGE]

        extra_kwargs = {
            'username': {REQUIRED: True},
            'room': {REQUIRED: True},
            'no_of_guests': {REQUIRED: True},
            'hotel': {REQUIRED: True},
            'check_in': {REQUIRED: True},
        }

    def create(self, validated_data):
        validated_data['username'] = self.context['request'].user
        Reservation.objects.create(**validated_data)
        return validated_data


    # def create(self, validated_data):
    #     current_user = {
    #         'username': self.context['request'].user,
    #         'no_of_guests': validated_data['no_of_guests'],
    #         'hotel': validated_data['hotel'],
    #         'room': validated_data['room'],
    #         'check_in': validated_data['check_in'],
    #         'check_out': validated_data['check_out'],
    #         'payment_type': validated_data['payment_type'],
    #     }
    #     Reservation.objects.create(**current_user)
    #     return validated_data

    def get_charge(self, obj):
        return obj.get_charge()
