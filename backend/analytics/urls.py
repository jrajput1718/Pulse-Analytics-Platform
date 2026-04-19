from django.urls import path

from .views import AnalyticsIngestView, DashboardSummaryView


urlpatterns = [
    path("analytics/collect/", AnalyticsIngestView.as_view(), name="analytics-collect"),
    path("analytics/dashboard/", DashboardSummaryView.as_view(), name="analytics-dashboard"),
]
