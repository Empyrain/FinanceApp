from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.render_main_page, name='main'),
    url(r'^login/$', views.render_login_page, name='login'),
    url(r'^sign-up/$', views.render_sign_up_page, name='signup'),
    url(r'^logout/$', views.render_logout_page, name='logout'),
    url(r'^users/$', views.render_users_page, name='users'),
    url(r'^users/(?P<username>[a-zA-Z]+)/statistic/$', views.render_statistic_page, name='statistic'),
    url(r'^users/(?P<username>[a-zA-Z]+)/$', views.render_user_page, name='user'),
    url(r'^users/(?P<username>[a-zA-Z]+)/(?P<account_name>[a-zA-Z01-9]+)/$', views.render_account_page, name='account'),
]
