from django.contrib import admin

from .models import AnalyticsEvent, VisitorSession


@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    list_display = (
        "session_key",
        "visitor_id",
        "site_domain",
        "started_at",
        "last_seen_at",
        "duration_seconds",
    )
    search_fields = ("session_key", "visitor_id", "site_domain", "path")
    list_filter = ("site_domain", "device_type", "country")


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "site_domain", "path", "created_at", "visitor_id")
    search_fields = ("site_domain", "path", "visitor_id", "session__session_key")
    list_filter = ("event_type", "site_domain", "device_type", "country")
