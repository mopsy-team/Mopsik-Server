# -*- coding: utf-8 -*-

from rest_framework import viewsets

from mops_api.models import MOP
from mops_api.serializers import MOPSerializer, TakenSerializer


class MOPViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super(MOPViewSet, self).list(request, *args, **kwargs)
        x = {}
        for i, mop in enumerate(response.data, 1):
            x[i] = mop
        response.data = x
        return response

    queryset = MOP.objects.all().order_by('id')
    serializer_class = MOPSerializer


class TakenViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super(TakenViewSet, self).list(request, *args, **kwargs)
        x = {}
        for i, mop in enumerate(response.data, 1):
            x[i] = mop
        response.data = x
        return response

    queryset = MOP.objects.all().order_by('id')
    serializer_class = TakenSerializer
