from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from .models import Profile, Hotel, HotelRoomType, Reservation
from constants import (USERNAME, MOBILE_NUMBER, ADDRESS, EMAIL, PASSWORD,
                       IS_SUPERUSER, IS_STAFF, REQUIRED,
                       NAME, CONTACT, ZIP, CITY, COUNTRY,
                       HOTEL, ROOM_NO, ROOM_TYPE, RATE, IS_AVAILABLE, PERSON_CAP,
                       ROOM, NO_OF_GUESTS, CHECK_IN, CHARGE, CHECK_OUT_DONE,
                       CHECK_OUT, PAYMENT_TYPE, PAYMENT_DATE, FIRST_NAME, LAST_NAME, PASSWORD2
                       )


class RegisterSerializer(serializers.ModelSerializer):
    """ registration for every user"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Profile
        fields = (USERNAME, FIRST_NAME, LAST_NAME, PASSWORD, PASSWORD2, EMAIL, MOBILE_NUMBER, ADDRESS)
        extra_kwargs = {
            'first_name': {REQUIRED: True},
            'last_name': {REQUIRED: True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Profile.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_number=validated_data['mobile_number'],
            address=validated_data['address']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
            'address': validated_data[ADDRESS],
            'email': validated_data[EMAIL],
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
                  CHECK_OUT_DONE, CHECK_OUT, PAYMENT_TYPE, CHARGE]

        read_only_fields = [USERNAME]

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
