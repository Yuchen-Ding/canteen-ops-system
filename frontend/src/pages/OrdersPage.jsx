import { useEffect, useMemo, useState } from 'react';
import { Eye, RefreshCw } from 'lucide-react';

import { fetchRecordDetail, fetchRecords } from '../services/api.js';

const customerTypeOptions = [
  { label: '员工', value: 'EMPLOYEE' },
  { label: '访客', value: 'VISITOR' },
];

const paymentStatusOptions = [
  { label: '待支付', value: 'PENDING' },
  { label: '已支付', value: 'PAID' },
  { label: '失败', value: 'FAILED' },
  { label: '已退款', value: 'REFUNDED' },
];

const orderStatusOptions = [
  { label: '已创建', value: 'CREATED' },
  { label: '已完成', value: 'COMPLETED' },
  { label: '已取消', value: 'CANCELLED' },
  { label: '已退款', value: 'REFUNDED' },
];

function labelOf(options, value) {
  return options.find((option) => option.value === value)?.label || value || '-';
}

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`;
}

export function OrdersPage() {
  const [filters, setFilters] = useState({ customer_type: '', payment_status: '', order_status: '' });
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ items: [], total: 0, page: 1, page_size: 20 });
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState('');

  const totalPages = useMemo(() => Math.max(1, Math.ceil(data.total / data.page_size)), [data]);

  const loadOrders = async (targetPage = page) => {
    setError('');
    try {
      const result = await fetchRecords('/api/v1/orders', { ...filters, page: targetPage, pageSize: 20 });
      setData(result);
    } catch (err) {
      setError(err.message || '订单加载失败');
    }
  };

  useEffect(() => {
    loadOrders();
  }, [page]);

  const submitSearch = (event) => {
    event.preventDefault();
    setPage(1);
    loadOrders(1);
  };

  const showDetail = async (orderId) => {
    setError('');
    try {
      setDetail(await fetchRecordDetail('/api/v1/orders', orderId));
    } catch (err) {
      setError(err.message || '订单详情加载失败');
    }
  };

  return (
    <section className="master-page">
      <div className="section-heading">
        <h2>订单管理</h2>
        <p>查看员工刷卡和访客扫码产生的订单，阶段 2 不提供退款和结算操作。</p>
      </div>

      <div className="toolbar">
        <form className="search-form" onSubmit={submitSearch}>
          <select value={filters.customer_type} onChange={(event) => setFilters({ ...filters, customer_type: event.target.value })}>
            <option value="">全部客户类型</option>
            {customerTypeOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <select value={filters.payment_status} onChange={(event) => setFilters({ ...filters, payment_status: event.target.value })}>
            <option value="">全部支付状态</option>
            {paymentStatusOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <select value={filters.order_status} onChange={(event) => setFilters({ ...filters, order_status: event.target.value })}>
            <option value="">全部订单状态</option>
            {orderStatusOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <button className="secondary-button" type="submit">查询</button>
        </form>
        <button className="icon-button" title="刷新" type="button" onClick={loadOrders}>
          <RefreshCw size={17} />
        </button>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      {detail ? (
        <div className="record-form">
          <div className="form-heading">
            <h3>订单详情：{detail.order.order_no}</h3>
            <button className="text-button" type="button" onClick={() => setDetail(null)}>关闭</button>
          </div>
          <div className="detail-grid">
            <span>客户类型：{labelOf(customerTypeOptions, detail.order.customer_type)}</span>
            <span>支付状态：{labelOf(paymentStatusOptions, detail.order.payment_status)}</span>
            <span>订单状态：{labelOf(orderStatusOptions, detail.order.order_status)}</span>
            <span>应付金额：{money(detail.order.payable_amount)}</span>
          </div>
          <div className="table-panel compact-table">
            <table>
              <thead>
                <tr>
                  <th>菜品</th>
                  <th>数量</th>
                  <th>单价</th>
                  <th>金额</th>
                </tr>
              </thead>
              <tbody>
                {detail.items.map((item) => (
                  <tr key={item.id}>
                    <td>{item.item_name_snapshot}</td>
                    <td>{item.quantity}</td>
                    <td>{money(item.unit_price)}</td>
                    <td>{money(item.amount)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : null}

      <div className="table-panel">
        <table>
          <thead>
            <tr>
              <th>订单号</th>
              <th>餐厅</th>
              <th>档口</th>
              <th>客户类型</th>
              <th>金额</th>
              <th>支付状态</th>
              <th>订单状态</th>
              <th>交易时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((order) => (
              <tr key={order.id}>
                <td>{order.order_no}</td>
                <td>{order.canteen_name || order.canteen_id}</td>
                <td>{order.stall_name || order.stall_id}</td>
                <td>{labelOf(customerTypeOptions, order.customer_type)}</td>
                <td>{money(order.payable_amount)}</td>
                <td>{labelOf(paymentStatusOptions, order.payment_status)}</td>
                <td>{labelOf(orderStatusOptions, order.order_status)}</td>
                <td>{order.transaction_time ? new Date(order.transaction_time).toLocaleString() : '-'}</td>
                <td>
                  <button className="icon-button" title="查看详情" type="button" onClick={() => showDetail(order.id)}>
                    <Eye size={16} />
                  </button>
                </td>
              </tr>
            ))}
            {data.items.length === 0 ? (
              <tr>
                <td className="empty-cell" colSpan="9">暂无订单</td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>

      <div className="pagination">
        <span>共 {data.total} 条，第 {page} / {totalPages} 页</span>
        <div>
          <button className="secondary-button" disabled={page <= 1} type="button" onClick={() => setPage(page - 1)}>上一页</button>
          <button className="secondary-button" disabled={page >= totalPages} type="button" onClick={() => setPage(page + 1)}>下一页</button>
        </div>
      </div>
    </section>
  );
}
