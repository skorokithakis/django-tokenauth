from django.conf.urls import url

from . import views


app_name = "tokenauth"
urlpatterns = [
    url(r'^login/$', views.token_post, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
]
