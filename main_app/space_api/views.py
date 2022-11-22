from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from space_api.models import Station

from space_api.serializer import StationsSerializer, StationCordinatSerializer


class StationsVeiwSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationsSerializer

    @action(methods=['get', 'post'], detail=True, name='state' )
    def state(self, request, pk):
        object= self.get_object()
        if object:
            serializer = StationCordinatSerializer(object)
        return Response(serializer.data)
