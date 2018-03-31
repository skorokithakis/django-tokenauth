from django.conf.urls import url

from . import views


app_name = "tokenauth"
urlpatterns = [
    url(r'^login/$', views.email_post, name="login"),
    url(r'^login/(?P<token>\w+)/$', views.token_post, name="login-token"),
    url(r'^logout/$', views.logout, name="logout"),
]
