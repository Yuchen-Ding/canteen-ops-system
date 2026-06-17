import { useEffect, useMemo, useState } from 'react';
import { RefreshCw } from 'lucide-react';

import { StatusBadge } from '../components/StatusBadge.jsx';
import { fetchRecords } from '../services/api.js';

const paymentMethodOptions = [
  { label: '员工卡', value: 'EMPLOYEE_CARD' },
  { label: '访客扫码', value: 'VISITOR_QR' },
  { label: '现金', value: 'CASH' },
  { label: '模拟支付宝', value: 'MOCK_ALIPAY' },
  { label: '模拟微信', value: 'MOCK_WECHAT' },
];

const paymentStatusOptions = [
  { label: '待支付', value: 'PENDING' },
  { label: '已支付', value: 'PAID' },
  { label: '失败', value: 'FAILED' },
  { label: '已退款', value: 'REFUNDED' },
];

function labelOf(options, value) {
  return options.find((option) => option.value === value)?.label || value || '-';
}

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`;
}

export function PaymentsPage() {
  const [filters, setFilters] = useState({ payment_method: '', payment_status: '' });
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ items: [], total: 0, page: 1, page_size: 20 });
  const [error, setError] = useState('');

  const totalPages = useMemo(() => Math.max(1, Math.ceil(data.total / data.page_size)), [data]);

  const loadPayments = async (targetPage = page) => {
    setError('');
    try {
      setData(await fetchRecords('/api/v1/payments', { ...filters, page: targetPage, pageSize: 20 }));
    } catch (err) {
      setError(err.message || '支付流水加载失败');
    }
  };

  useEffect(() => {
    loadPayments();
  }, [page]);

  const submitSearch = (event) => {
    event.preventDefault();
    setPage(1);
    loadPayments(1);
  };

  const resetFilters = () => {
    const nextFilters = { payment_method: '', payment_status: '' };
    setFilters(nextFilters);
    setPage(1);
    setError('');
    fetchRecords('/api/v1/payments', { ...nextFilters, page: 1, pageSize: 20 })
      .then(setData)
      .catch((err) => setError(err.message || '支付流水加载失败'));
  };

  return (
    <section className="master-page">
      <div className="page-header">
        <div>
          <h1>支付流水</h1>
          <p>查看员工卡和访客扫码消费产生的支付流水。</p>
        </div>
      </div>

      <div className="toolbar filter-bar">
        <form className="search-form" onSubmit={submitSearch}>
          <select value={filters.payment_method} onChange={(event) => setFilters({ ...filters, payment_method: event.target.value })}>
            <option value="">全部支付方式</option>
            {paymentMethodOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <select value={filters.payment_status} onChange={(event) => setFilters({ ...filters, payment_status: event.target.value })}>
            <option value="">全部支付状态</option>
            {paymentStatusOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <button className="primary-button" type="submit">查询</button>
          <button className="secondary-button" type="button" onClick={resetFilters}>重置</button>
        </form>
        <button className="icon-button" title="刷新" type="button" onClick={loadPayments}>
          <RefreshCw size={17} />
        </button>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      <div className="table-panel">
        <table>
          <thead>
            <tr>
              <th>支付流水号</th>
              <th>订单号</th>
              <th>金额</th>
              <th>支付方式</th>
              <th>支付状态</th>
              <th>支付时间</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((payment) => (
              <tr key={payment.id}>
                <td>{payment.payment_no}</td>
                <td>{payment.order_no}</td>
                <td>{money(payment.payment_amount)}</td>
                <td>{labelOf(paymentMethodOptions, payment.payment_method)}</td>
                <td><StatusBadge value={payment.payment_status} label={labelOf(paymentStatusOptions, payment.payment_status)} /></td>
                <td>{payment.paid_at ? new Date(payment.paid_at).toLocaleString() : '-'}</td>
              </tr>
            ))}
            {data.items.length === 0 ? (
              <tr>
                <td className="empty-cell" colSpan="6">暂无支付流水</td>
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
