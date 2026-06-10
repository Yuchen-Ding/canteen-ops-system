import { useEffect, useState } from 'react';
import { BadgeDollarSign, ClipboardList, RefreshCcw, TrendingUp, UserRound, UsersRound } from 'lucide-react';

import { fetchReport } from '../services/api.js';

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`;
}

function RankingList({ title, items, valueKey, valueFormatter }) {
  return (
    <section className="ranking-panel">
      <h3>{title}</h3>
      <ol>
        {items.map((item) => (
          <li key={`${item.id || item.name}-${item.name}`}>
            <span>{item.name}</span>
            <strong>{valueFormatter(item[valueKey])}</strong>
          </li>
        ))}
        {items.length === 0 ? <li className="empty-ranking">暂无数据</li> : null}
      </ol>
    </section>
  );
}

export function Dashboard() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  const loadDashboard = async () => {
    setError('');
    try {
      setReport(await fetchReport('/api/v1/reports/dashboard'));
    } catch (err) {
      setError(err.message || '运营看板加载失败');
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const metrics = report
    ? [
        { title: '今日订单数', value: report.today_order_count, icon: ClipboardList },
        { title: '今日营业额', value: money(report.today_revenue), icon: BadgeDollarSign },
        { title: '今日退款金额', value: money(report.today_refund_amount), icon: RefreshCcw },
        { title: '今日净收入', value: money(report.today_net_revenue), icon: TrendingUp },
        { title: '员工订单数', value: report.today_employee_order_count, icon: UsersRound },
        { title: '访客订单数', value: report.today_visitor_order_count, icon: UserRound },
      ]
    : [];

  return (
    <section className="dashboard">
      <div className="section-heading dashboard-heading">
        <div>
          <h2>运营看板</h2>
          <p>{report ? `${report.report_date} 企业餐厅运营数据` : '加载今日运营数据'}</p>
        </div>
        <button className="secondary-button" type="button" onClick={loadDashboard}>刷新数据</button>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      <div className="report-metrics dashboard-metrics">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <article className="metric-block metric-with-icon" key={metric.title}>
              <Icon size={20} />
              <span>{metric.title}</span>
              <strong>{metric.value}</strong>
            </article>
          );
        })}
      </div>

      {report ? (
        <div className="ranking-grid">
          <RankingList title="餐厅收入排行" items={report.revenue_by_canteen || []} valueKey="revenue" valueFormatter={money} />
          <RankingList title="档口收入排行" items={report.revenue_by_stall || []} valueKey="revenue" valueFormatter={money} />
          <RankingList title="热门菜品" items={report.top_dishes || []} valueKey="quantity" valueFormatter={(value) => `${value} 份`} />
        </div>
      ) : null}
    </section>
  );
}
