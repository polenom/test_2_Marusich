import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from space_api.models import Station

client = APIClient()


@pytest.mark.django_db
def test_get_station(user):
    response = client.get('/api/v1/stations/')
    data = response.data
    assert data == []
    assert user.username == 'alukard'


@pytest.mark.parametrize('url,method,status,date', [
    ['/api/v1/stations/', 'get', 200, {}],
    ['/api/v1/stations/', 'post', 201, {"name": "bild"}],
    ['/api/v1/stations/', 'put', 405, {}],
    ['/api/v1/stations/', 'patch', 405, {}],
    ['/api/v1/stations/', 'delete', 405, {}],
])
@pytest.mark.django_db
def test_methods_stations(url, method, status, date):
    response = getattr(client, method)(url, data=date)
    assert response.status_code == status


@pytest.mark.parametrize('url,method,status,date', [
    ['/api/v1/stations/', 'get', 200, {}],
    ['/api/v1/stations/', 'post', 405, {}],
    ['/api/v1/stations/', 'put', 200, {"name": "123"}],
    ['/api/v1/stations/', 'patch', 200, {"name": "123"}],
    ['/api/v1/stations/', 'delete', 204, {}],
])
@pytest.mark.django_db
def test_methods_station(url, method, status, date, station):
    response = getattr(client, method)(f'{url}{station.id}/', date)
    assert response.status_code == status


@pytest.mark.parametrize('url,method,status,date', [
    ['/api/v1/stations/', 'get', 200, {}],
    ['/api/v1/stations/', 'post', 201, {"user": "alukard", "axis": "y", "distance": -110}],
    ['/api/v1/stations/', 'put', 405, {}],
    ['/api/v1/stations/', 'patch', 405, {}],
    ['/api/v1/stations/', 'delete', 405, {}],
])
@pytest.mark.django_db
def test_methods_station_state(url, method, status, date, station, user):
    response = getattr(client, method)(f'{url}{station.id}/state/', date)
    assert response.status_code == status


@pytest.mark.django_db
def test_create_station():
    response = client.post('/api/v1/stations/', data={"name": "alukard"})
    assert response.data['name'] == 'alukard'
    assert response.data['status'] == 'running'
    assert response.data['create_date'] is not None
    assert response.data['broke_date'] is None
    response = client.post('/api/v1/stations/', data={"name": "alukard"})
    assert response.status_code == 400
    response = client.post('/api/v1/stations/', data={"name": ""})
    assert response.status_code == 400
    response = client.post('/api/v1/stations/', data={"name1": "fd"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_stations(station):
    response = client.get('/api/v1/stations/')
    assert len(response.data) == 1
    client.post('/api/v1/stations/', data={"name": "1"})
    client.post('/api/v1/stations/', data={"name": "2"})
    client.post('/api/v1/stations/', data={"name": "2"})
    response = client.get('/api/v1/stations/')
    assert len(response.data) == 3
    assert '1' in map(lambda a: a['name'], response.data)
    assert '2' in map(lambda a: a['name'], response.data)
    assert 'bild' in map(lambda a: a['name'], response.data)


@pytest.mark.django_db
def test_update_station(station):
    response = client.patch(f'/api/v1/stations/{station.pk}/', data={"name": "asd"})
    print(123, Station.objects.all().count())
    assert response.data['name'] == "asd"
    response = client.put(f'/api/v1/stations/{station.pk}/', data={"name": "dsa", "status": "broken"})
    assert response.data['name'] == "dsa"
    response = client.get('/api/v1/stations/')
    assert len(response.data) == 1
    assert response.data[0]["name"] == "dsa"
    assert response.data[0]["status"] == "running"


@pytest.mark.django_db
def test_delete_station(station):
    response = client.delete(f'/api/v1/stations/{123321321}/')
    assert response.status_code == 404
    client.delete(f'/api/v1/stations/{station.pk}/')
    assert len(Station.objects.all()) == 0


@pytest.mark.django_db
def test_get_post_coordinates(station, user):
    url = f'/api/v1/stations/{station.pk}/state/'
    response = client.get(url)
    assert response.data == {'x': 100, 'y': 100, 'z': 100}
    response = client.post(url, data={"user": user.username, "axis": "y", "distance": -100})
    assert response.data == {'x': 100, 'y': 0, 'z': 100}
    response = client.get(url)
    assert response.data == {'x': 100, 'y': 0, 'z': 100}
    response = client.post(url, data={"user": user.username, "axis": "y", "distance": 0})
    assert response.status_code == 400
    response = client.post(url, data={"user": user.username, "axis": "y", "distance": 'fds'})
    assert response.status_code == 400
    response = client.post(url, data={"user": user.username, "axis": "e", "distance": 10})
    assert response.status_code == 400


@pytest.mark.django_db
def test_run_brok(station, user):
    url = f'/api/v1/stations/{station.pk}/'
    response = client.post(url + 'state/', data={"user": user.username, "axis": "y", "distance": -110})
    assert response.data == {'x': 100, 'y': -10, 'z': 100}
    response = client.get(url)
    assert response.data['status'] == 'broken'
    client.post(url + 'state/', data={"user": user.username, "axis": "y", "distance": 20})
    response = client.get(url)
    assert response.data['status'] == 'broken'


@pytest.mark.django_db
def test_create_user():
    count = User.objects.all().count()
    client.post('/api/v1/user/', data={"username": "bbffdfddfdffds",
                                       "password": "Qwerty123",
                                       "email": "aaa@vk.by"})
    assert User.objects.all().count() == count + 1
