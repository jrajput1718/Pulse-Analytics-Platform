const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export async function fetchDashboard(days, site) {
  const params = new URLSearchParams({ days: String(days) });
  if (site) {
    params.append("site", site);
  }

  const response = await fetch(`${API_BASE}/analytics/dashboard/?${params}`);
  if (!response.ok) {
    throw new Error("Unable to load analytics dashboard");
  }
  return response.json();
}

export function getTrackingSnippet() {
  return `<script>
  (() => {
    const endpoint = "${API_BASE}/analytics/collect/";
    const sessionKey = sessionStorage.getItem("pulse_session_key") || crypto.randomUUID();
    const visitorKey = localStorage.getItem("pulse_visitor_key") || crypto.randomUUID();
    sessionStorage.setItem("pulse_session_key", sessionKey);
    localStorage.setItem("pulse_visitor_key", visitorKey);
    const agent = navigator.userAgent.toLowerCase();

    const detectDevice = () => {
      if (/tablet|ipad/.test(agent)) return "tablet";
      if (/mobi|android/.test(agent)) return "mobile";
      return "desktop";
    };

    const detectBrowser = () => {
      if (agent.includes("edg")) return "Edge";
      if (agent.includes("chrome")) return "Chrome";
      if (agent.includes("firefox")) return "Firefox";
      if (agent.includes("safari")) return "Safari";
      return "Other";
    };

    const detectOS = () => {
      if (agent.includes("win")) return "Windows";
      if (agent.includes("mac")) return "macOS";
      if (agent.includes("android")) return "Android";
      if (agent.includes("iphone") || agent.includes("ipad")) return "iOS";
      if (agent.includes("linux")) return "Linux";
      return "Other";
    };

    const payload = {
      event_type: "pageview",
      site_domain: window.location.hostname,
      page_url: window.location.href,
      path: window.location.pathname,
      page_title: document.title,
      referrer: document.referrer,
      session_key: sessionKey,
      visitor_key: visitorKey,
      device_type: detectDevice(),
      browser: detectBrowser(),
      os: detectOS(),
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      event_duration: 0
    };

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    let startedAt = Date.now();
    const flush = (eventType) => {
      navigator.sendBeacon(
        endpoint,
        new Blob(
          [
            JSON.stringify({
              ...payload,
              event_type: eventType,
              event_duration: Math.floor((Date.now() - startedAt) / 1000)
            })
          ],
          { type: "application/json" }
        )
      );
    };

    window.addEventListener("beforeunload", () => flush("session_end"));
  })();
</script>`;
}
