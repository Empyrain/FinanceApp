from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.response_index, name='index'),
    url(r'^info/$', views.response_info, name='info'),
]
