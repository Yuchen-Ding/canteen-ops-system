export function EmptyState({ text = '暂无数据' }) {
  return <div className="empty-state">{text}</div>;
}

function toNumber(value) {
  return Number(value || 0);
}

export function TrendBarChart({ title, items, valueKey, labelKey = 'date', formatter = (value) => value }) {
  const maxValue = Math.max(...items.map((item) => toNumber(item[valueKey])), 0);

  return (
    <section className="chart-card">
      <div className="chart-card-header">
        <h3>{title}</h3>
      </div>
      {items.length === 0 || maxValue === 0 ? (
        <EmptyState />
      ) : (
        <div className="trend-chart">
          {items.map((item) => {
            const value = toNumber(item[valueKey]);
            const height = Math.max(8, Math.round((value / maxValue) * 120));
            return (
              <div className="trend-column" key={item[labelKey]}>
                <div className="trend-bar-wrap">
                  <div className="trend-bar" style={{ height }} title={`${item[labelKey]} ${formatter(value)}`} />
                </div>
                <strong>{formatter(value)}</strong>
                <span>{String(item[labelKey]).slice(5)}</span>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}

export function HorizontalBarChart({ title, items, valueKey, labelKey = 'name', formatter = (value) => value }) {
  const maxValue = Math.max(...items.map((item) => toNumber(item[valueKey])), 0);

  return (
    <section className="chart-card">
      <div className="chart-card-header">
        <h3>{title}</h3>
      </div>
      {items.length === 0 || maxValue === 0 ? (
        <EmptyState />
      ) : (
        <div className="mini-bar-chart">
          {items.map((item, index) => {
            const value = toNumber(item[valueKey]);
            return (
              <div className="mini-bar-row" key={`${item[labelKey]}-${index}`}>
                <div className="mini-bar-meta">
                  <span>{item[labelKey]}</span>
                  <strong>{formatter(value)}</strong>
                </div>
                <div className="mini-bar-track">
                  <div className="mini-bar-fill" style={{ width: `${Math.max(4, (value / maxValue) * 100)}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}

export function DistributionBars({ title, items, valueKey, labelKey = 'label', formatter = (value) => value }) {
  const total = items.reduce((sum, item) => sum + toNumber(item[valueKey]), 0);

  return (
    <section className="chart-card">
      <div className="chart-card-header">
        <h3>{title}</h3>
        {total > 0 ? <span>合计 {formatter(total)}</span> : null}
      </div>
      {items.length === 0 || total === 0 ? (
        <EmptyState />
      ) : (
        <div className="distribution-list">
          {items.map((item, index) => {
            const value = toNumber(item[valueKey]);
            const percent = total > 0 ? Math.round((value / total) * 100) : 0;
            return (
              <div className="distribution-row" key={`${item[labelKey]}-${index}`}>
                <div className="distribution-meta">
                  <span>{item[labelKey]}</span>
                  <strong>{formatter(value)} · {percent}%</strong>
                </div>
                <div className="distribution-track">
                  <div className="distribution-fill" style={{ width: `${Math.max(3, percent)}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
