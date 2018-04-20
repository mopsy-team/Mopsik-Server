# -*- coding: utf-8 -*-
from django.db import models

MOP_TYPE_CHOICES = (
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
)

TECHNICAL_CLASS_CHOICES = (
    ('0', 'A'),
    ('1', 'S'),
)

MAX_STRING_LENGTH = 100
MAX_ROAD_NUMBER_LENGTH = 10
MAX_PHONE_NUMBER_LENGTH = 9


class Operator(models.Model):
    name = models.CharField(max_length=MAX_STRING_LENGTH, primary_key=True)
    phone = models.CharField(max_length=MAX_PHONE_NUMBER_LENGTH, default='')
    email = models.CharField(max_length=MAX_STRING_LENGTH, default='')
    permission = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " " + self.phone + " " + self.email


class MOP(models.Model):
    id = models.AutoField(primary_key=True)
    number_in_excel = models.IntegerField(default=0)
    department = models.CharField(max_length=MAX_STRING_LENGTH, default='')
    town = models.CharField(max_length=MAX_STRING_LENGTH, default='')
    type = models.CharField(max_length=3, choices=MOP_TYPE_CHOICES, default='1')
    title = models.CharField(max_length=MAX_STRING_LENGTH, default='')
    # system wgs84
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    # system 92
    x_92 = models.FloatField(default=0)
    y_92 = models.FloatField(default=0)
    road_technical_class = models.CharField(max_length=1, choices=TECHNICAL_CLASS_CHOICES, default='1')
    road_number = models.CharField(max_length=MAX_ROAD_NUMBER_LENGTH, default='')
    direction = models.CharField(max_length=MAX_STRING_LENGTH, default='')
    operator = models.ForeignKey('Operator', on_delete=None)

    passenger_places = models.IntegerField(default=0)
    taken_passenger_places = models.IntegerField(default=0)
    truck_places = models.IntegerField(default=0)
    taken_truck_places = models.IntegerField(default=0)
    bus_dedicated_places = models.IntegerField(default=0)
    taken_bus_dedicated_places = models.IntegerField(default=0)

    security = models.BooleanField(default=False)
    fence = models.BooleanField(default=False)
    monitoring = models.BooleanField(default=False)
    lighting = models.BooleanField(default=False)
    petrol_station = models.BooleanField(default=False)
    dangerous_cargo_places = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=False)
    sleeping_places = models.BooleanField(default=False)
    toilets = models.BooleanField(default=False)
    car_wash = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)

    chainage = models.CharField(max_length=MAX_STRING_LENGTH, default='')
    # not included from excel provided by GDDKiA:
    # turnoff - zjazd

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('x', 'y', 'title', 'town')
