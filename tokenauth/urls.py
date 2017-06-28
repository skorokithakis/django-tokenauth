from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/$', views.token_post, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
]
