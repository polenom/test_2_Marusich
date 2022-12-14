import pytest

from space_api.services import UserDataClass, create_user

from space_api.models import Station

from rest_framework.test import APIClient


@pytest.fixture
def user():
    user_dc = UserDataClass(
        username="alukard",
        password="Alukard1234",
        email="alukr@tut.by"
    )
    user = create_user(user_dc)
    return user


@pytest.fixture
def station():
    return Station.objects.create(name="bild")


@pytest.fixture
def client():
    return APIClient()
