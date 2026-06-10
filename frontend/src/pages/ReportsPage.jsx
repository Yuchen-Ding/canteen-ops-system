import { useEffect, useState } from 'react';
import { RefreshCw } from 'lucide-react';

import { fetchReport } from '../services/api.js';

function localDateValue() {
  const now = new Date();
  const offset = now.getTimezoneOffset() * 60000;
  return new Date(now.getTime() - offset).toISOString().slice(0, 10);
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
          <thead>
            <tr>
              <th>名称</th>
              <th>{kind === 'dish' ? '销量' : '订单数'}</th>
              <th>金额</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={`${item.id || item.name}-${index}`}>
                <td>{item.name}</td>
                <td>{kind === 'dish' ? item.quantity : item.order_count}</td>
                <td>{money(item.revenue)}</td>
              </tr>
            ))}
            {items.length === 0 ? (
              <tr><td className="empty-cell" colSpan="3">暂无数据</td></tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export function ReportsPage({ mode }) {
  const isDaily = mode === 'daily';
  const [period, setPeriod] = useState(isDaily ? localDateValue() : localDateValue().slice(0, 7));
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    setPeriod(isDaily ? localDateValue() : localDateValue().slice(0, 7));
    setReport(null);
  }, [isDaily]);

  const loadReport = async () => {
    setError('');
    try {
      setReport(
        await fetchReport(
          isDaily ? '/api/v1/reports/daily' : '/api/v1/reports/monthly',
          isDaily ? { report_date: period } : { month: period },
        ),
      );
    } catch (err) {
      setError(err.message || '报表加载失败');
    }
  };

  useEffect(() => {
    loadReport();
  }, [period, isDaily]);

  const metrics = report
    ? isDaily
      ? [
          ['订单数', report.total_orders],
          ['营业额', money(report.total_revenue)],
          ['退款金额', money(report.total_refund_amount)],
          ['净收入', money(report.net_revenue)],
          ['员工订单', report.employee_orders],
          ['访客订单', report.visitor_orders],
        ]
      : [
          ['订单数', report.month_order_count],
          ['营业额', money(report.month_revenue)],
          ['退款金额', money(report.month_refund_amount)],
          ['净收入', money(report.month_net_revenue)],
          ['员工订单', report.employee_consumption_summary?.order_count || 0],
          ['访客订单', report.visitor_consumption_summary?.order_count || 0],
        ]
    : [];

  return (
    <section className="master-page">
      <div className="section-heading">
        <h2>{isDaily ? '运营日报' : '运营月报'}</h2>
        <p>基于订单、订单明细和成功退款记录生成基础运营统计。</p>
      </div>

      <div className="toolbar">
        <label className="report-period">
          <span>{isDaily ? '报表日期' : '报表月份'}</span>
          <input type={isDaily ? 'date' : 'month'} value={period} onChange={(event) => setPeriod(event.target.value)} />
        </label>
        <button className="icon-button" title="刷新" type="button" onClick={loadReport}>
          <RefreshCw size={17} />
        </button>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      {report ? (
        <>
          <div className="report-metrics">
            {metrics.map(([label, value]) => (
              <article className="metric-block" key={label}>
                <span>{label}</span>
                <strong>{value}</strong>
              </article>
            ))}
          </div>
          <div className="report-grid">
            <RankingTable title="餐厅收入" items={report.revenue_by_canteen || []} />
            <RankingTable title="档口收入" items={report.revenue_by_stall || []} />
            <RankingTable title="热门菜品" items={report.top_dishes || []} kind="dish" />
          </div>
        </>
      ) : null}
    </section>
  );
}
