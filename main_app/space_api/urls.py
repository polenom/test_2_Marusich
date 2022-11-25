from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from space_api.views import StationsVeiwSet, CreateUser

router = routers.SimpleRouter()
router.register(r'stations', StationsVeiwSet)
print(router.urls)

urlpatterns = [
    path('',include(router.urls)),
    path('user/', CreateUser.as_view())
]
