from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.render_main_page, name='main'),
    url(r'^account/(?P<name>[a-zA-Z]+)$', views.render_account_page, name='account'),
]
