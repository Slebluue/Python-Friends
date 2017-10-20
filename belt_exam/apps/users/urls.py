from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^user/(?P<id>\d+)$', views.show, name="show"),
    url(r'^add/(?P<id>\d+)$', views.add, name="add"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name="remove"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^login$', views.login, name="login"),
    url(r'^$', views.index, name="home"),
    url(r'^friends$', views.friends, name="friends"),
    url(r'^register$', views.register, name="register")
]
