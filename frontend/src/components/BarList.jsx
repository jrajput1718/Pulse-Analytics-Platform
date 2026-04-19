export default function BarList({ title, items, valueKey, labelKey, formatter }) {
  const max = Math.max(...items.map((entry) => entry[valueKey] || 0), 1);

  return (
    <section className="panel">
      <div className="panel__header">
        <h3>{title}</h3>
      </div>
      <div className="bar-list">
        {items.length ? (
          items.map((item) => {
            const value = item[valueKey] || 0;
            const label = item[labelKey] || "Direct / Unknown";
            return (
              <div className="bar-list__row" key={`${title}-${label}`}>
                <div className="bar-list__copy">
                  <strong>{label}</strong>
                  <span>{formatter ? formatter(value, item) : value}</span>
                </div>
                <div className="bar-list__track">
                  <div
                    className="bar-list__fill"
                    style={{ width: `${(value / max) * 100}%` }}
                  />
                </div>
              </div>
            );
          })
        ) : (
          <div className="empty-state">No data available yet.</div>
        )}
      </div>
    </section>
  );
}
