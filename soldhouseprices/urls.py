from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timeseries', views.get_time_series, name='timeseries'),
    path('histogram', views.get_histogram, name='histogram')
]
