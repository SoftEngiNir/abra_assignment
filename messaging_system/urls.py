from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def root(request):
    return HttpResponse("This is the root URL for the abra home assignment")


urlpatterns = [
    path("", root, name="index"),
    path("messages/", include("messaging.urls")),
    path("admin/", admin.site.urls),
]
