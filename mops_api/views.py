# -*- coding: utf-8 -*-

from rest_framework import viewsets

from mops_api.models import MOP
from mops_api.serializers import MOPSerializer, TakenSerializer


class MOPViewSet(viewsets.ModelViewSet):
    queryset = MOP.objects.all().order_by('id')
    serializer_class = MOPSerializer


class TakenViewSet(viewsets.ModelViewSet):
    queryset = MOP.objects.all().order_by('id')
    serializer_class = TakenSerializer
