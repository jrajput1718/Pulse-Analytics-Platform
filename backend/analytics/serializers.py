from rest_framework import serializers


class AnalyticsEventIngestSerializer(serializers.Serializer):
    event_type = serializers.ChoiceField(
        choices=["pageview", "heartbeat", "session_end"],
        default="pageview",
    )
    site_domain = serializers.CharField(max_length=255)
    page_url = serializers.CharField(max_length=2048)
    path = serializers.CharField(max_length=1024)
    page_title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    referrer = serializers.CharField(max_length=1024, required=False, allow_blank=True)
    session_key = serializers.CharField(max_length=128)
    visitor_key = serializers.CharField(max_length=128, required=False, allow_blank=True)
    device_type = serializers.CharField(max_length=50, required=False, allow_blank=True)
    browser = serializers.CharField(max_length=100, required=False, allow_blank=True)
    os = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    region = serializers.CharField(max_length=100, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    timezone = serializers.CharField(max_length=100, required=False, allow_blank=True)
    event_duration = serializers.IntegerField(required=False, min_value=0)
    occurred_at = serializers.DateTimeField(required=False)


class DashboardFilterSerializer(serializers.Serializer):
    days = serializers.IntegerField(required=False, min_value=1, max_value=90, default=7)
    site = serializers.CharField(required=False, max_length=255)
