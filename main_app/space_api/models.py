import datetime
import json

import pytz
from django.contrib.auth.models import User
from django.db import models


class Station(models.Model):
    SPACE_STATUS = (('r', 'running'),
                    ('b', 'broken'))

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=SPACE_STATUS, default='r')
    create_date = models.DateTimeField(auto_now_add=True)
    broke_date = models.DateTimeField(blank=True, null=True)
    axis = models.CharField(max_length=50, default='[100, 100, 100]')

    def get_cordinat_dict(self) -> dict:
        x, y, z = json.loads(self.axis)
        return {'x': x, 'y': y ,'z': z}

    def set_cordinat(self,**kwargs):
        cor_obj = self.get_cordinat_dict()
        for key in kwargs.keys():
            cor_obj[key] = kwargs[key]
        self.axis = f"[{cor_obj['x']}, {cor_obj['y']}, {cor_obj['z']}]"

    @property
    def x(self):
        print(self.get_cordinat_dict()['x'])
        return self.get_cordinat_dict()['x']

    @x.setter
    def x(self, value):
        self.set_cordinat(x=value)

    @property
    def y(self):
        print(self.get_cordinat_dict()['y'])
        return self.get_cordinat_dict()['y']

    @y.setter
    def y(self, value):
        self.set_cordinat(y=value)

    @property
    def z(self):
        print(self.get_cordinat_dict()['z'])
        return self.get_cordinat_dict()['z']

    @z.setter
    def z(self, value):
        self.set_cordinat(z=value)


    def save(self, *args, **kwargs):
        if '-' in self.axis and self.status == 'r':
            self.status = 'b'
            self.broke_date = datetime.datetime.now(pytz.timezone('UTC'))
        return super(Station, self).save(*args, **kwargs)


class Instructions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructions')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='changes')
    distance = models.FloatField()
    axis = models.CharField(max_length=50)
