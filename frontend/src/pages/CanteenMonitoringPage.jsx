import { useEffect, useState } from 'react';
import { RefreshCw } from 'lucide-react';

import { StatusBadge } from '../components/StatusBadge.jsx';
import { getCanteenMonitoringOverview } from '../services/api.js';

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`;
}

const masterLabels = {
  canteen_count: '餐厅数量',
  stall_count: '档口数量',
  dish_count: '菜品数量',
  meal_package_count: '套餐数量',
  employee_count: '员工数量',
  visitor_count: '访客数量',
  device_count: 'POS 设备数量',
};

const statusLabels = {
  active_canteen_count: '启用餐厅',
  active_stall_count: '启用档口',
  available_dish_count: '可售菜品',
  online_device_count: '在线设备',
  offline_device_count: '离线设备',
  inactive_employee_count: '停用员工',
  inactive_visitor_count: '停用访客',
};

export function CanteenMonitoringPage() {
  const [overview, setOverview] = useState(null);
  const [error, setError] = useState('');

  const loadOverview = async () => {
    setError('');
    try {
      setOverview(await getCanteenMonitoringOverview());
    } catch (err) {
      setError(err.message || '食堂基础监控加载失败');
    }
  };

  useEffect(() => {
    loadOverview();
  }, []);

  const business = overview?.today_business_summary;

  return (
    <section className="master-page">
      <div className="page-header">
        <div>
          <h1>食堂基础监控</h1>
          <p>查看餐厅、档口、菜品、员工、访客和设备的基础规模与状态。</p>
        </div>
        <button className="secondary-button" type="button" onClick={loadOverview}>
          <RefreshCw size={16} /> 刷新
        </button>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      {overview ? (
        <>
          <h3 className="band-title">基础规模</h3>
          <div className="monitoring-metrics">
            {Object.entries(masterLabels).map(([key, label]) => (
              <article className="metric-block" key={key}>
                <span>{label}</span>
                <strong>{overview.master_data_summary[key]}</strong>
              </article>
            ))}
          </div>

          <h3 className="band-title">状态概览</h3>
          <div className="monitoring-metrics">
            {Object.entries(statusLabels).map(([key, label]) => (
              <article className="metric-block" key={key}>
                <span>{label}</span>
                <strong>{overview.status_summary[key]}</strong>
              </article>
            ))}
          </div>

          <h3 className="band-title">今日业务概览</h3>
          <div className="report-metrics">
            {[
              ['今日订单', business.today_order_count],
              ['今日收入', money(business.today_revenue)],
              ['今日退款', money(business.today_refund_amount)],
              ['今日净收入', money(business.today_net_revenue)],
              ['员工订单', business.today_employee_order_count],
              ['访客订单', business.today_visitor_order_count],
            ].map(([label, value]) => (
              <article className="metric-block" key={label}><span>{label}</span><strong>{value}</strong></article>
            ))}
          </div>

          <div className="monitoring-tables">
            <section>
              <h3>餐厅与档口规模</h3>
              <div className="table-panel compact-table">
                <table><thead><tr><th>餐厅</th><th>城市</th><th>状态</th><th>档口数</th></tr></thead>
                  <tbody>{overview.canteen_list.map((item) => (
                    <tr key={item.id}><td>{item.name}</td><td>{item.city}</td><td><StatusBadge value={item.status} /></td><td>{item.stall_count}</td></tr>
                  ))}</tbody>
                </table>
              </div>
            </section>
            <section>
              <h3>档口与菜品规模</h3>
              <div className="table-panel compact-table">
                <table><thead><tr><th>档口</th><th>餐厅</th><th>状态</th><th>菜品数</th></tr></thead>
                  <tbody>{overview.stall_list.map((item) => (
                    <tr key={item.id}><td>{item.name}</td><td>{item.canteen_name}</td><td><StatusBadge value={item.status} /></td><td>{item.dish_count}</td></tr>
                  ))}</tbody>
                </table>
              </div>
            </section>
          </div>

          <section>
            <h3>POS 设备状态</h3>
            <div className="table-panel">
              <table><thead><tr><th>设备</th><th>类型</th><th>餐厅</th><th>档口</th><th>位置</th><th>状态</th></tr></thead>
                <tbody>{overview.device_list.map((item) => (
                  <tr key={item.id}>
                    <td>{item.device_name}</td><td>{item.device_type}</td><td>{item.canteen_name}</td>
                    <td>{item.stall_name || '-'}</td><td>{item.location || '-'}</td><td><StatusBadge value={item.status} /></td>
                  </tr>
                ))}</tbody>
              </table>
            </div>
          </section>
        </>
      ) : null}
    </section>
  );
}
