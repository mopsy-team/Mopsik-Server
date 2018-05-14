# -*- coding: utf-8 -*-
from django.http import JsonResponse
from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json

from mops_api.converter.converter import puwg92_do_wgs84
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