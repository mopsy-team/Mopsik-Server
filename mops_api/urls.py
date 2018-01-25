# -*- coding: utf-8 -*-
from django.conf.urls import url
from mops_api.views import mops_view, taken_view, index_view

urlpatterns = [
    url(r'^$', index_view),
    url(r'mops', mops_view),
    url(r'taken', taken_view),
]
