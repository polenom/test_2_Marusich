from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response

from space_api.models import Station

from space_api.serializer import StationsSerializer, StationCordinatSerializer, InstructionsSerializer, UserSerializer



class StationsVeiwSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationsSerializer

    @extend_schema(
        description='Получение информации о станции',
        summary='Получение информации о станции',
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Получение списка станциях",
        summary="Получение списка станциях",
        responses={200: StationsSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description='Cоздание станции',
        summary='Cоздание станции',
        request=StationsSerializer,
        responses={201: StationsSerializer(many=False),
                   400: None},

    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description='Удаление станции',
        summary='Удаление станции',
        responses={204: None,
                   400: None},

    )
    def destroy(self, request, *args, **kwargs):
        return super(StationsVeiwSet, self).destroy(request, *args, **kwargs)

    @extend_schema(
        description='Изменение имя станции',
        summary='Изменение имя станции',
        request=StationsSerializer,
        responses={201: StationsSerializer(many=False),
                   404: None},

    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description="Получение позиции станции",
        summary="Получение позиции станции",
        responses={200: StationCordinatSerializer(many=False),
                   404: None},
    )
    @action(methods=['get'], detail=True, name='state')
    def state(self, request, pk):
        object = self.get_object()
        if object:
            serializer = StationCordinatSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Изменение позиции станции",
        summary="Изменение позиции станции",
        request=InstructionsSerializer,
        responses={200: StationCordinatSerializer(many=False),
                   400: None},
    )
    @state.mapping.post
    def post_state(self, request, pk):
        data = {**request.data, 'station': pk}
        serializer = InstructionsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.station_coordinate, status=status.HTTP_201_CREATED)


class CreateUser(views.APIView):

    @extend_schema(
        description="Создать пользователя",
        summary="Создать пользователя",
        request=UserSerializer,
        responses={201: UserSerializer(many=False),
                   400: None}, )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
