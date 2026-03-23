from django.contrib import admin
from django.urls import path, include

from config.views import healthcheck, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("", home, name="home"),
    path("references/", include("apps.references.urls")),
    path("transactions/", include("apps.transactions.urls")),
]
