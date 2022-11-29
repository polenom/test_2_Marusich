import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from space_api.models import Station
from django.urls import reverse

URL_GET_STATIONS = reverse('stations-list')


@pytest.mark.django_db
def test_get_station(user, client):
    response = client.get(URL_GET_STATIONS)
    data = response.data
    assert data == []
    assert user.username == 'alukard'


@pytest.mark.parametrize('url,method,status,date', [
    [URL_GET_STATIONS, 'get', 200, {}],
    [URL_GET_STATIONS, 'post', 201, {"name": "bild"}],
    [URL_GET_STATIONS, 'put', 405, {}],
    [URL_GET_STATIONS, 'patch', 405, {}],
    [URL_GET_STATIONS, 'delete', 405, {}],
])
@pytest.mark.django_db
def test_methods_stations(url, method, status, date, client):
    response = getattr(client, method)(url, data=date)
    assert response.status_code == status


@pytest.mark.parametrize('url,method,status,date', [
    [URL_GET_STATIONS, 'get', 200, {}],
    [URL_GET_STATIONS, 'post', 405, {}],
    [URL_GET_STATIONS, 'put', 200, {"name": "123"}],
    [URL_GET_STATIONS, 'patch', 200, {"name": "123"}],
    [URL_GET_STATIONS, 'delete', 204, {}],
])
@pytest.mark.django_db
def test_methods_station(url, method, status, date, station, client):
    response = getattr(client, method)(f'{url}{station.id}/', date)
    assert response.status_code == status


@pytest.mark.parametrize('url,method,status,date', [
    [URL_GET_STATIONS, 'get', 200, {}],
    [URL_GET_STATIONS, 'post', 201, {"user": "alukard", "axis": "y", "distance": -110}],
    [URL_GET_STATIONS, 'put', 405, {}],
    [URL_GET_STATIONS, 'patch', 405, {}],
    [URL_GET_STATIONS, 'delete', 405, {}],
])
@pytest.mark.django_db
def test_methods_station_state(url, method, status, date, station, user, client):
    response = getattr(client, method)(f'{url}{station.id}/state/', date)
    assert response.status_code == status


@pytest.mark.django_db
def test_create_station(client):
    response = client.post(URL_GET_STATIONS, data={"name": "alukard"})
    assert response.data['name'] == 'alukard'
    assert response.data['status'] == 'running'
    assert response.data['create_date'] is not None
    assert response.data['broke_date'] is None
    response = client.post(URL_GET_STATIONS, data={"name": "alukard"})
    assert response.status_code == 400
    response = client.post(URL_GET_STATIONS, data={"name": ""})
    assert response.status_code == 400
    response = client.post(URL_GET_STATIONS, data={"name1": "fd"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_stations(station, client):
    response = client.get(URL_GET_STATIONS)
    assert len(response.data) == 1
    client.post(URL_GET_STATIONS, data={"name": "1"})
    client.post(URL_GET_STATIONS, data={"name": "2"})
    client.post(URL_GET_STATIONS, data={"name": "2"})
    response = client.get(URL_GET_STATIONS)
    assert len(response.data) == 3
    assert '1' in map(lambda a: a['name'], response.data)
    assert '2' in map(lambda a: a['name'], response.data)
    assert 'bild' in map(lambda a: a['name'], response.data)


@pytest.mark.django_db
def test_update_station(station, client):
    detail_url = reverse('stations-detail', args=[station.pk])
    response = client.patch(detail_url, data={"name": "asd"})
    assert response.data['name'] == "asd"
    response = client.put(detail_url, data={"name": "dsa", "status": "broken"})
    assert response.data['name'] == "dsa"
    response = client.get(URL_GET_STATIONS)
    assert len(response.data) == 1
    assert response.data[0]["name"] == "dsa"
    assert response.data[0]["status"] == "running"


@pytest.mark.django_db
def test_delete_station(station, client):
    response = client.delete(reverse('stations-detail', args=[321323123133]))
    assert response.status_code == 404
    client.delete(reverse('stations-detail', args=[station.pk]))
    assert len(Station.objects.all()) == 0


@pytest.mark.django_db
def test_get_post_coordinates(station, user, client):
    url = reverse('stations-state', args=[station.pk])
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
def test_run_brok(station, user, client):
    url = reverse('stations-detail', args=[station.pk])
    response = client.post(url + 'state/', data={"user": user.username, "axis": "y", "distance": -110})
    assert response.data == {'x': 100, 'y': -10, 'z': 100}
    response = client.get(url)
    assert response.data['status'] == 'broken'
    client.post(url + 'state/', data={"user": user.username, "axis": "y", "distance": 20})
    response = client.get(url)
    assert response.data['status'] == 'broken'


@pytest.mark.django_db
def test_create_user(client):
    count = User.objects.all().count()
    client.post(reverse('create_user'), data={"username": "bbffdfddfdffds",
                                       "password": "Qwerty123",
                                       "email": "aaa@vk.by"})
    assert User.objects.all().count() == count + 1
