from django.contrib import admin
from django.urls import include, path

from config.views import healthcheck
from apps.transactions.views.list import CashflowRecordListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("health/", healthcheck, name="healthcheck"),
    path("", CashflowRecordListView.as_view(), name="home"),
    path("references/", include("apps.references.urls")),
    path("transactions/", include("apps.transactions.urls")),
]
