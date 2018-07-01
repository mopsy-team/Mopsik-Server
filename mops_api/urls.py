# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from mops_api import views

router = routers.DefaultRouter()
router.register(r'mops', views.MOPViewSet, base_name='mops')
router.register(r'taken', views.TakenViewSet, base_name='taken')
#router.register(r'wsg_to_92', views.wgs_to_puwg92, base_name='wgs_to_puwg92')
#router.register(r'92_to_wsg', views.puwg92_to_wgs84, base_name='puwg92_to_wgs')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'wsg_to_92', views.wgs_to_puwg92),
    url(r'92_to_wsg', views.puwg92_to_wgs),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

