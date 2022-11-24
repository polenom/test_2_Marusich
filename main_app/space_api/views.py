from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, generics, status, views
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from space_api.models import Station

from space_api.serializer import StationsSerializer, StationCordinatSerializer, InstructionsSerializer

from space_api.services import UserDataClass, create_user


class StationsVeiwSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationsSerializer

    @action(methods=['get', 'post'], detail=True, name='state' )
    def state(self, request, pk):
        return getattr(self, f'{request.method.lower()}_state')(request, pk)


    def get_state(self, request, pk):
        object = self.get_object()
        if object:
            serializer = StationCordinatSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post_state(self, request, pk):
        data = {**request.data, 'station': pk}
        serializer= InstructionsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.station_coordinate, status=status.HTTP_201_CREATED)


