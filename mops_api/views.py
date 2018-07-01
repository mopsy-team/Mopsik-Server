# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json

from mops_api.converter.converter import puwg92_to_wgs84, wgs84_to_puwg92
from mops_api.models import MOP
from mops_api.serializers import MOPSerializer, TakenSerializer


class MOPViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super(MOPViewSet, self).list(request, *args, **kwargs)
        x = {}
        for mop in response.data:
            x[mop['id']] = mop
        response.data = x
        return response

    queryset = MOP.objects.all().order_by('id')
    serializer_class = MOPSerializer


class TakenViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super(TakenViewSet, self).list(request, *args, **kwargs)
        x = {}
        for mop in response.data:
            x[mop['id']] = mop
        response.data = x
        return response

    queryset = MOP.objects.all().order_by('id')
    serializer_class = TakenSerializer


def wgs_to_puwg92(request):
    if request.method == 'GET':
        x = float(request.GET.get('x', False))
        y = float(request.GET.get('y', False))
        (_, x1, y1) = wgs84_to_puwg92(x, y)
        return JsonResponse({'x': x1, 'y': y1})


def puwg92_to_wgs(request):
    if request.method == 'GET':
        x = float(request.GET.get('x', False))
        y = float(request.GET.get('y', False))
        (x1, y1) = puwg92_to_wgs84(x, y)
        return JsonResponse({'x': x1, 'y': y1})
