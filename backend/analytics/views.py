from datetime import timedelta
import hashlib

from django.conf import settings
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnalyticsEvent, VisitorSession
from .serializers import AnalyticsEventIngestSerializer, DashboardFilterSerializer


def _client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def _visitor_id(request, provided_key):
    raw_value = provided_key or _client_ip(request)
    salted = f"{settings.ANALYTICS_VISITOR_SALT}:{raw_value}"
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()


class AnalyticsIngestView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AnalyticsEventIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        occurred_at = payload.get("occurred_at", timezone.now())
        visitor_id = _visitor_id(request, payload.get("visitor_key", ""))
        session, created = VisitorSession.objects.get_or_create(
            session_key=payload["session_key"],
            defaults={
                "visitor_id": visitor_id,
                "site_domain": payload["site_domain"],
                "landing_page": payload["page_url"],
                "path": payload["path"],
                "referrer": payload.get("referrer", ""),
                "device_type": payload.get("device_type", ""),
                "browser": payload.get("browser", ""),
                "os": payload.get("os", ""),
                "country": payload.get("country", ""),
                "region": payload.get("region", ""),
                "city": payload.get("city", ""),
                "timezone": payload.get("timezone", ""),
                "started_at": occurred_at,
                "last_seen_at": occurred_at,
                "duration_seconds": payload.get("event_duration", 0) or 0,
                "pageview_count": 0,
            },
        )

        if not created:
            session.site_domain = payload["site_domain"]
            session.path = payload["path"]
            session.last_seen_at = occurred_at
            session.referrer = payload.get("referrer", session.referrer)
            session.device_type = payload.get("device_type", session.device_type)
            session.browser = payload.get("browser", session.browser)
            session.os = payload.get("os", session.os)
            session.country = payload.get("country", session.country)
            session.region = payload.get("region", session.region)
            session.city = payload.get("city", session.city)
            session.timezone = payload.get("timezone", session.timezone)

        if payload["event_type"] == "pageview":
            session.pageview_count += 1

        session.duration_seconds = max(
            session.duration_seconds,
            int((occurred_at - session.started_at).total_seconds()),
            payload.get("event_duration", 0) or 0,
        )
        session.is_bounce = session.pageview_count <= 1
        session.save()

        AnalyticsEvent.objects.create(
            session=session,
            event_type=payload["event_type"],
            site_domain=payload["site_domain"],
            page_url=payload["page_url"],
            path=payload["path"],
            page_title=payload.get("page_title", ""),
            referrer=payload.get("referrer", ""),
            device_type=payload.get("device_type", ""),
            browser=payload.get("browser", ""),
            os=payload.get("os", ""),
            country=payload.get("country", ""),
            region=payload.get("region", ""),
            city=payload.get("city", ""),
            timezone=payload.get("timezone", ""),
            visitor_id=visitor_id,
            event_duration=payload.get("event_duration", 0) or 0,
        )

        return Response(
            {
                "status": "ok",
                "session_created": created,
                "visitor_id": visitor_id,
            },
            status=status.HTTP_201_CREATED,
        )


class DashboardSummaryView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        serializer = DashboardFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data

        start_date = timezone.now() - timedelta(days=filters.get("days", 7) - 1)
        events = AnalyticsEvent.objects.filter(created_at__gte=start_date)
        sessions = VisitorSession.objects.filter(last_seen_at__gte=start_date)

        site = filters.get("site")
        if site:
            events = events.filter(site_domain=site)
            sessions = sessions.filter(site_domain=site)

        total_page_views = events.filter(event_type="pageview").count()
        unique_visitors = sessions.values("visitor_id").distinct().count()
        total_sessions = sessions.count()
        avg_session_duration = (
            sessions.aggregate(value=Avg("duration_seconds")).get("value") or 0
        )
        bounce_rate = 0
        if total_sessions:
            bounce_rate = round(
                (sessions.filter(is_bounce=True).count() / total_sessions) * 100,
                1,
            )

        views_over_time = list(
            events.filter(event_type="pageview")
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(page_views=Count("id"), visitors=Count("visitor_id", distinct=True))
            .order_by("day")
        )

        top_pages = list(
            events.filter(event_type="pageview")
            .values("path", "page_title")
            .annotate(
                page_views=Count("id"),
                unique_visitors=Count("visitor_id", distinct=True),
                avg_time=Avg("event_duration"),
            )
            .order_by("-page_views")[:10]
        )

        referrers = list(
            events.exclude(referrer="")
            .values("referrer")
            .annotate(visits=Count("id"))
            .order_by("-visits")[:8]
        )

        devices = list(
            sessions.values("device_type")
            .annotate(visits=Count("id"))
            .order_by("-visits")
        )

        geography = list(
            sessions.exclude(country="")
            .values("country")
            .annotate(visits=Count("id"))
            .order_by("-visits")[:8]
        )

        browsers = list(
            sessions.values("browser")
            .annotate(visits=Count("id"))
            .order_by("-visits")[:6]
        )

        sites = list(
            VisitorSession.objects.values("site_domain")
            .annotate(sessions=Count("id"))
            .order_by("-sessions")
        )

        return Response(
            {
                "summary": {
                    "page_views": total_page_views,
                    "unique_visitors": unique_visitors,
                    "sessions": total_sessions,
                    "avg_session_duration": round(avg_session_duration, 1),
                    "bounce_rate": bounce_rate,
                },
                "views_over_time": views_over_time,
                "top_pages": top_pages,
                "referrers": referrers,
                "devices": devices,
                "geography": geography,
                "browsers": browsers,
                "sites": sites,
            }
        )
