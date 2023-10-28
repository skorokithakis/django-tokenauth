from django.urls import include, path


urlpatterns = [
    path("auth/", include("tokenauth.urls", namespace="tokenauth")),
]
