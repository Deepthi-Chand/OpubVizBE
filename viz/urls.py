from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^chart/$', views.ChartView.as_view(), name='demo'),
    url(r'^download/$', views.DownloadView.as_view(), name='demo'),
    url(r'^index/$', views.IndexView.as_view(), name='demo'),
]