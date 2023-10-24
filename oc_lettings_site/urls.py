from django.contrib import admin
from django.urls import path, include

from . import views


# Trigger an uncaught error, used to test Sentry error logging
def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


urlpatterns = [
    path("", views.index, name="index"),
    path("lettings/", include("lettings.urls")),
    path("profiles/", include("profiles.urls")),
    path("admin/", admin.site.urls),
    # path to call the function view that will trigger an uncaught error
    path("sentry_debug/", trigger_error),
]
