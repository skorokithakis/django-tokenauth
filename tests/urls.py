from django.contrib import admin
from django.http import HttpResponse
from django.urls import include
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("tokenauth.urls", namespace="tokenauth")),
    path(
        "authenticated/",
        lambda request: HttpResponse(
            "authenticated" if request.user.is_authenticated else "unauthenticated"
        ),
    ),
]
