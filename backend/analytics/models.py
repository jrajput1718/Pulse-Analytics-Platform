from django.db import models


class VisitorSession(models.Model):
    session_key = models.CharField(max_length=128, unique=True)
    visitor_id = models.CharField(max_length=128, db_index=True)
    site_domain = models.CharField(max_length=255, db_index=True)
    landing_page = models.CharField(max_length=1024, blank=True)
    path = models.CharField(max_length=1024, blank=True, db_index=True)
    referrer = models.CharField(max_length=1024, blank=True)
    device_type = models.CharField(max_length=50, blank=True, db_index=True)
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, db_index=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField()
    last_seen_at = models.DateTimeField()
    duration_seconds = models.PositiveIntegerField(default=0)
    is_bounce = models.BooleanField(default=True)
    pageview_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-last_seen_at"]

    def __str__(self):
        return f"{self.site_domain} {self.session_key}"


class AnalyticsEvent(models.Model):
    EVENT_TYPES = [
        ("pageview", "Page View"),
        ("heartbeat", "Heartbeat"),
        ("session_end", "Session End"),
    ]

    session = models.ForeignKey(
        VisitorSession,
        on_delete=models.CASCADE,
        related_name="events",
    )
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES, default="pageview")
    site_domain = models.CharField(max_length=255, db_index=True)
    page_url = models.CharField(max_length=2048)
    path = models.CharField(max_length=1024, db_index=True)
    page_title = models.CharField(max_length=255, blank=True)
    referrer = models.CharField(max_length=1024, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, db_index=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)
    visitor_id = models.CharField(max_length=128, db_index=True)
    event_duration = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} {self.path}"
