from collections import OrderedDict

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty, set_value, SkipField, get_error_detail

from space_api.models import Station, Instructions


class ChoiceStatusField(serializers.ChoiceField):
    def to_representation(self, value):
        return self.choices[value]


class StationsSerializer(serializers.ModelSerializer):
    status = ChoiceStatusField(choices=Station.SPACE_STATUS, read_only=True)

    class Meta:
        model = Station
        fields = ('name', 'id', 'status', 'create_date', 'broke_date')
        read_only = ('id', 'create_date', 'broke_date')


class StationCordinatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('x', 'y', 'z')
        read_only = ('x', 'y', 'z')


# class StationCordinatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Station
#         fields = ('x', 'y', 'z')


class MyUserSerializer(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        queryset = self.get_queryset()
        try:
            if isinstance(data, bool):
                raise TypeError
            return queryset.get(username=data)
        except ObjectDoesNotExist:
            raise ValidationError(f'Invalid username \"{data}\" - object does not exist.')
        except (TypeError, ValueError):
            raise ValidationError(f'Incorrect type. Expected username value, received {type(data).__name__}.')


class InstructionsSerializer(serializers.ModelSerializer):
    station_coordinate = None
    user = MyUserSerializer(queryset=User.objects.all(), many=False)

    class Meta:
        model = Instructions
        fields = ('user', 'station', 'axis', 'distance')

    def validate_axis(self, attrs):
        if attrs not in ['x', 'y', 'z']:
            raise serializers.ValidationError('This field should be x, y or z')
        return attrs

    def validate_distance(self, attrs):
        if not isinstance(attrs, int):
            raise serializers.ValidationError('This field should be integer')
        if attrs == 0:
            raise serializers.ValidationError('This field shouldn\'t be 0')
        return attrs

    def create(self, validated_data):
        key, value = validated_data['axis'], validated_data['distance']
        validated_data['station'].change_coordinates(key, value)
        self.station_coordinate = validated_data['station'].get_coordinates()
        return super(InstructionsSerializer, self).create(validated_data)
