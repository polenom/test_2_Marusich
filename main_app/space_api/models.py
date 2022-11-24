import datetime
import json

import pytz
from django.contrib.auth.models import User
from django.db import models


class Station(models.Model):
    SPACE_STATUS = (('r', 'running'),
                    ('b', 'broken'))

    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=1, choices=SPACE_STATUS, default='r')
    create_date = models.DateTimeField(auto_now_add=True)
    broke_date = models.DateTimeField(blank=True, null=True)
    x = models.IntegerField(default=100)
    y = models.IntegerField(default=100)
    z = models.IntegerField(default=100)

    def save(self, *args, **kwargs):
        if (self.x < 0 or self.y < 0 or self.z < 0) and self.status == 'r':
            self.status = 'b'
            self.broke_date = datetime.datetime.now(pytz.timezone('UTC'))
        return super(Station, self).save(*args, **kwargs)

    def change_coordinates(self, key, value):
        now_value = getattr(self, key)
        setattr(self, key, now_value + value)
        return self.save()

    def get_coordinates(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}


class Instructions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructions')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='changes')
    distance = models.IntegerField()
    axis = models.CharField(max_length=1)
