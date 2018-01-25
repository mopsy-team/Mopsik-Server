# -*- coding: utf-8 -*-
import random

from django.http import JsonResponse
from django.shortcuts import render

from mops_api.models import MOP, Operator


def randomize_free_places():
    for mop in MOP.objects.all():
        mop.free_bus_dedicated_places = random.randint(0, mop.bus_dedicated_places)
        mop.free_truck_places = random.randint(0, mop.truck_places)
        mop.free_passenger_places= random.randint(0, mop.passenger_places)
        mop.save()

def mops_view(request):
    randomize_free_places()

    data = {}
    for mop in MOP.objects.values():
        dict = mop

        dict['available'] = {'car' : mop['passenger_places'], 'truck' : mop['truck_places'], 'bus' : mop['bus_dedicated_places']}
        dict['taken'] = {'car' : mop['free_passenger_places'], 'truck' : mop['free_truck_places'], 'bus' : mop['free_bus_dedicated_places']}
        dict['title'] = mop['name']
        dict['description'] = 'tu będzie opis mopa'
        dict['coords'] = {'longitude' : mop['y'], 'latitude' : mop['x']}
        operator, _ = Operator.objects.get_or_create(name=mop['operator_id'])
        dict['operator_name'] = operator.name
        dict['operator_email'] = operator.email
        dict['operator_permission'] = operator.permission
        data[mop['id']] = dict
    return JsonResponse(data)


def taken_view(request):
    randomize_free_places()

    data = {}
    for mop in MOP.objects.values():
        dict = {}
        #dict['available'] = {'car' : mop['passenger_places'], 'truck' : mop['truck_places'], 'bus' : mop['bus_dedicated_places']}
        dict['taken'] = {'car' : mop['free_passenger_places'], 'truck' : mop['free_truck_places'], 'bus' : mop['free_bus_dedicated_places']}
        data[mop['id']] = dict
    return JsonResponse(data)

def index_view(request):
    return render(request, 'index.html')