export default function MetricCard({ label, value, accent, suffix = "" }) {
  return (
    <article className="metric-card">
      <div className="metric-card__glow" style={{ background: accent }} />
      <p className="metric-card__label">{label}</p>
      <h3 className="metric-card__value">
        {value}
        {suffix}
      </h3>
    </article>
  );
}
