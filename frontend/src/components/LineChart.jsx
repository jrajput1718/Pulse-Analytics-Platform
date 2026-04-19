function formatNumber(value) {
  return new Intl.NumberFormat().format(value);
}

export default function LineChart({ data }) {
  if (!data.length) {
    return <div className="empty-state">No page view data available yet.</div>;
  }

  const width = 620;
  const height = 240;
  const padding = 28;
  const maxValue = Math.max(...data.map((item) => item.page_views), 1);

  const points = data
    .map((item, index) => {
      const x =
        padding + (index * (width - padding * 2)) / Math.max(data.length - 1, 1);
      const y =
        height -
        padding -
        (item.page_views / maxValue) * (height - padding * 2);
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div className="chart-shell">
      <svg viewBox={`0 0 ${width} ${height}`} className="line-chart">
        <polyline
          fill="none"
          stroke="#ff7a3d"
          strokeWidth="4"
          strokeLinejoin="round"
          strokeLinecap="round"
          points={points}
        />
        {data.map((item, index) => {
          const x =
            padding +
            (index * (width - padding * 2)) / Math.max(data.length - 1, 1);
          const y =
            height -
            padding -
            (item.page_views / maxValue) * (height - padding * 2);
          return <circle key={item.day} cx={x} cy={y} r="4.5" fill="#fff5eb" />;
        })}
      </svg>
      <div className="chart-labels">
        {data.map((item) => (
          <div key={item.day} className="chart-label">
            <span>
              {new Date(item.day).toLocaleDateString(undefined, {
                month: "short",
                day: "numeric",
              })}
            </span>
            <strong>{formatNumber(item.page_views)}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}
