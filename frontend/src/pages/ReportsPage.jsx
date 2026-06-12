import { useEffect, useMemo, useState } from 'react';
import { RefreshCw } from 'lucide-react';

import { fetchReport, getYearlyReport } from '../services/api.js';

function currentDateParts() {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
  const parts = Object.fromEntries(formatter.formatToParts(new Date()).map((part) => [part.type, part.value]));
  return {
    day: `${parts.year}-${parts.month}-${parts.day}`,
    month: `${parts.year}-${parts.month}`,
    year: parts.year,
  };
}

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`;
}

function RankingTable({ title, items, kind = 'revenue' }) {
  return (
    <section className="report-section">
      <h3>{title}</h3>
      <div className="table-panel compact-table">
        <table>
          <thead><tr><th>名称</th><th>{kind === 'dish' ? '销量' : '订单数'}</th><th>金额</th></tr></thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={`${item.id || item.name}-${index}`}>
                <td>{item.name}</td>
                <td>{kind === 'dish' ? item.quantity : item.order_count}</td>
                <td>{money(item.revenue)}</td>
              </tr>
            ))}
            {items.length === 0 ? <tr><td className="empty-cell" colSpan="3">暂无数据</td></tr> : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export function ReportsPage() {
  const defaults = useMemo(currentDateParts, []);
  const [periodType, setPeriodType] = useState('day');
  const [periodValues, setPeriodValues] = useState(defaults);
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  const period = periodValues[periodType];
  const loadReport = async () => {
    setError('');
    try {
      const result =
        periodType === 'day'
          ? await fetchReport('/api/v1/reports/daily', { report_date: period })
          : periodType === 'month'
            ? await fetchReport('/api/v1/reports/monthly', { month: period })
            : await getYearlyReport(period);
      setReport(result);
    } catch (err) {
      setReport(null);
      setError(err.message || '报表加载失败');
    }
  };

  useEffect(() => {
    loadReport();
  }, [periodType, period]);

  const updatePeriod = (value) => setPeriodValues((current) => ({ ...current, [periodType]: value }));
  const metrics = report
    ? periodType === 'day'
      ? [['订单数', report.total_orders], ['营业额', money(report.total_revenue)], ['退款金额', money(report.total_refund_amount)], ['净收入', money(report.net_revenue)], ['员工订单', report.employee_orders], ['访客订单', report.visitor_orders]]
      : periodType === 'month'
        ? [['订单数', report.month_order_count], ['营业额', money(report.month_revenue)], ['退款金额', money(report.month_refund_amount)], ['净收入', money(report.month_net_revenue)], ['员工订单', report.employee_consumption_summary?.order_count || 0], ['访客订单', report.visitor_consumption_summary?.order_count || 0]]
        : [['订单数', report.year_order_count], ['营业额', money(report.year_revenue)], ['退款金额', money(report.year_refund_amount)], ['净收入', money(report.year_net_revenue)], ['员工订单', report.employee_consumption_summary?.order_count || 0], ['访客订单', report.visitor_consumption_summary?.order_count || 0]]
    : [];

  return (
    <section className="master-page">
      <div className="section-heading">
        <h2>报表中心</h2>
        <p>按日、月、年查看订单、收入、退款、净收入和经营排行。</p>
      </div>
      <div className="toolbar report-toolbar">
        <div className="segmented-control">
          {[['day', '日'], ['month', '月'], ['year', '年']].map(([value, label]) => (
            <button className={periodType === value ? 'active' : ''} key={value} type="button" onClick={() => setPeriodType(value)}>{label}</button>
          ))}
        </div>
        <label className="report-period">
          <span>统计周期</span>
          {periodType === 'year' ? (
            <input min="2000" max="2100" type="number" value={period} onChange={(event) => updatePeriod(event.target.value.slice(0, 4))} />
          ) : (
            <input type={periodType === 'day' ? 'date' : 'month'} value={period} onChange={(event) => updatePeriod(event.target.value)} />
          )}
        </label>
        <button className="icon-button" title="刷新" type="button" onClick={loadReport}><RefreshCw size={17} /></button>
      </div>
      {error ? <div className="error-banner">{error}</div> : null}
      {report ? (
        <>
          <div className="report-metrics">{metrics.map(([label, value]) => (
            <article className="metric-block" key={label}><span>{label}</span><strong>{value}</strong></article>
          ))}</div>
          {periodType === 'year' ? (
            <section className="report-section yearly-table">
              <h3>月度趋势</h3>
              <div className="table-panel"><table><thead><tr><th>月份</th><th>订单数</th><th>营业额</th><th>退款</th><th>净收入</th></tr></thead>
                <tbody>{(report.revenue_by_month || []).map((item) => (
                  <tr key={item.month}><td>{item.month}</td><td>{item.order_count}</td><td>{money(item.revenue)}</td><td>{money(item.refund_amount)}</td><td>{money(item.net_revenue)}</td></tr>
                ))}</tbody>
              </table></div>
            </section>
          ) : null}
          <div className="report-grid">
            <RankingTable title="餐厅收入" items={report.revenue_by_canteen || []} />
            <RankingTable title="档口收入" items={report.revenue_by_stall || []} />
            <RankingTable title="热门菜品" items={report.top_dishes || []} kind="dish" />
          </div>
        </>
      ) : !error ? <div className="empty-report">暂无数据</div> : null}
    </section>
  );
}
