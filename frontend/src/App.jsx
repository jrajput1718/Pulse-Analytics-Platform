import { useEffect, useState } from "react";
import BarList from "./components/BarList";
import LineChart from "./components/LineChart";
import MetricCard from "./components/MetricCard";
import { fetchDashboard, getTrackingSnippet } from "./services/api";

const accentPalette = ["#ff7a3d", "#ffd166", "#5dd39e", "#2ec4b6", "#7f95ff"];

function formatDuration(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  if (!mins) {
    return `${secs}s`;
  }
  return `${mins}m ${secs}s`;
}

function formatNumber(value) {
  return new Intl.NumberFormat().format(value || 0);
}

export default function App() {
  const [days, setDays] = useState(7);
  const [site, setSite] = useState("");
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");
        const data = await fetchDashboard(days, site);
        if (!cancelled) {
          setDashboard(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadDashboard();
    return () => {
      cancelled = true;
    };
  }, [days, site]);

  const metrics = dashboard?.summary
    ? [
        {
          label: "Page Views",
          value: formatNumber(dashboard.summary.page_views),
        },
        {
          label: "Unique Visitors",
          value: formatNumber(dashboard.summary.unique_visitors),
        },
        {
          label: "Sessions",
          value: formatNumber(dashboard.summary.sessions),
        },
        {
          label: "Avg. Session",
          value: formatDuration(dashboard.summary.avg_session_duration),
        },
        {
          label: "Bounce Rate",
          value: dashboard.summary.bounce_rate,
          suffix: "%",
        },
      ]
    : [];

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Pulse Analytics</p>
          <h1>Traffic intelligence for modern websites.</h1>
          <p className="hero__copy">
            Collect page views, sessions, referrers, devices, and geographic
            trends through a Django API and monitor everything from a React
            dashboard.
          </p>
        </div>
        <div className="hero__controls">
          <label>
            Date Range
            <select value={days} onChange={(event) => setDays(Number(event.target.value))}>
              <option value={7}>Last 7 days</option>
              <option value={14}>Last 14 days</option>
              <option value={30}>Last 30 days</option>
            </select>
          </label>
          <label>
            Site Filter
            <select value={site} onChange={(event) => setSite(event.target.value)}>
              <option value="">All tracked sites</option>
              {dashboard?.sites?.map((entry) => (
                <option key={entry.site_domain} value={entry.site_domain}>
                  {entry.site_domain}
                </option>
              ))}
            </select>
          </label>
        </div>
      </section>

      {loading ? <div className="loading">Loading dashboard...</div> : null}
      {error ? <div className="error-banner">{error}</div> : null}

      {dashboard && !loading ? (
        <>
          <section className="metrics-grid">
            {metrics.map((metric, index) => (
              <MetricCard
                key={metric.label}
                label={metric.label}
                value={metric.value}
                suffix={metric.suffix}
                accent={`radial-gradient(circle at top, ${accentPalette[index]}, transparent 70%)`}
              />
            ))}
          </section>

          <section className="panel panel--feature">
            <div className="panel__header">
              <div>
                <p className="panel__eyebrow">Traffic Trend</p>
                <h2>Page views over time</h2>
              </div>
            </div>
            <LineChart data={dashboard.views_over_time} />
          </section>

          <section className="dashboard-grid">
            <BarList
              title="Top Pages"
              items={dashboard.top_pages}
              labelKey="path"
              valueKey="page_views"
              formatter={(value, item) =>
                `${formatNumber(value)} views - ${formatNumber(item.unique_visitors)} visitors`
              }
            />
            <BarList
              title="Referrers"
              items={dashboard.referrers}
              labelKey="referrer"
              valueKey="visits"
              formatter={(value) => `${formatNumber(value)} visits`}
            />
            <BarList
              title="Device Types"
              items={dashboard.devices}
              labelKey="device_type"
              valueKey="visits"
              formatter={(value) => `${formatNumber(value)} sessions`}
            />
            <BarList
              title="Geography"
              items={dashboard.geography}
              labelKey="country"
              valueKey="visits"
              formatter={(value) => `${formatNumber(value)} sessions`}
            />
            <BarList
              title="Browsers"
              items={dashboard.browsers}
              labelKey="browser"
              valueKey="visits"
              formatter={(value) => `${formatNumber(value)} sessions`}
            />
            <section className="panel">
              <div className="panel__header">
                <h3>Tracking Snippet</h3>
              </div>
              <p className="snippet-copy">
                Drop this script into any site you want to measure. It creates
                stable visitor and session IDs in the browser and posts events
                to the Django ingestion API.
              </p>
              <pre className="snippet-block">
                <code>{getTrackingSnippet()}</code>
              </pre>
            </section>
          </section>
        </>
      ) : null}
    </main>
  );
}
