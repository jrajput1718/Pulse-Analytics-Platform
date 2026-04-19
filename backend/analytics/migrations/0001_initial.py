from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VisitorSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(max_length=128, unique=True)),
                ("visitor_id", models.CharField(db_index=True, max_length=128)),
                ("site_domain", models.CharField(db_index=True, max_length=255)),
                ("landing_page", models.CharField(blank=True, max_length=1024)),
                ("path", models.CharField(blank=True, db_index=True, max_length=1024)),
                ("referrer", models.CharField(blank=True, max_length=1024)),
                ("device_type", models.CharField(blank=True, db_index=True, max_length=50)),
                ("browser", models.CharField(blank=True, max_length=100)),
                ("os", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(blank=True, db_index=True, max_length=100)),
                ("region", models.CharField(blank=True, max_length=100)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("timezone", models.CharField(blank=True, max_length=100)),
                ("started_at", models.DateTimeField()),
                ("last_seen_at", models.DateTimeField()),
                ("duration_seconds", models.PositiveIntegerField(default=0)),
                ("is_bounce", models.BooleanField(default=True)),
                ("pageview_count", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["-last_seen_at"]},
        ),
        migrations.CreateModel(
            name="AnalyticsEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_type", models.CharField(choices=[("pageview", "Page View"), ("heartbeat", "Heartbeat"), ("session_end", "Session End")], default="pageview", max_length=30)),
                ("site_domain", models.CharField(db_index=True, max_length=255)),
                ("page_url", models.CharField(max_length=2048)),
                ("path", models.CharField(db_index=True, max_length=1024)),
                ("page_title", models.CharField(blank=True, max_length=255)),
                ("referrer", models.CharField(blank=True, max_length=1024)),
                ("device_type", models.CharField(blank=True, max_length=50)),
                ("browser", models.CharField(blank=True, max_length=100)),
                ("os", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(blank=True, db_index=True, max_length=100)),
                ("region", models.CharField(blank=True, max_length=100)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("timezone", models.CharField(blank=True, max_length=100)),
                ("visitor_id", models.CharField(db_index=True, max_length=128)),
                ("event_duration", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("session", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="analytics.visitorsession")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
