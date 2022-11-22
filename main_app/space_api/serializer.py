from rest_framework import serializers

from space_api.models import Station


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
        fields = ('name', 'id', 'axis')
        read_only = ('id', 'axis')


class StationCordinatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('x', 'y', 'z')
