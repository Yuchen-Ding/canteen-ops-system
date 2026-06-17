import { useEffect, useMemo, useState } from 'react';
import { Eye, RefreshCw, Search } from 'lucide-react';

import { StatusBadge } from '../components/StatusBadge.jsx';
import { fetchRecordDetail, fetchRecords } from '../services/api.js';

const refundStatusOptions = [
  { label: '处理中', value: 'PENDING' },
  { label: '退款成功', value: 'SUCCESS' },
  { label: '退款失败', value: 'FAILED' },
];

function labelOf(value) {
  return refundStatusOptions.find((option) => option.value === value)?.label || value || '-';
}

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`;
}

export function RefundsPage() {
  const [keyword, setKeyword] = useState('');
  const [refundStatus, setRefundStatus] = useState('');
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ items: [], total: 0, page: 1, page_size: 20 });
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState('');

  const totalPages = useMemo(() => Math.max(1, Math.ceil(data.total / data.page_size)), [data]);

  const loadRefunds = async (targetPage = page) => {
    setError('');
    try {
      setData(
        await fetchRecords('/api/v1/refunds', {
          keyword,
          refund_status: refundStatus,
          page: targetPage,
          pageSize: 20,
        }),
      );
    } catch (err) {
      setError(err.message || '退款记录加载失败');
    }
  };

  useEffect(() => {
    loadRefunds();
  }, [page]);

  const submitSearch = (event) => {
    event.preventDefault();
    setPage(1);
    loadRefunds(1);
  };

  const resetFilters = () => {
    setKeyword('');
    setRefundStatus('');
    setPage(1);
    setError('');
    fetchRecords('/api/v1/refunds', { keyword: '', refund_status: '', page: 1, pageSize: 20 })
      .then(setData)
      .catch((err) => setError(err.message || '退款记录加载失败'));
  };

  const showDetail = async (refundId) => {
    setError('');
    try {
      setDetail(await fetchRecordDetail('/api/v1/refunds', refundId));
    } catch (err) {
      setError(err.message || '退款详情加载失败');
    }
  };

  return (
    <section className="master-page">
      <div className="page-header">
        <div>
          <h1>退款管理</h1>
          <p>查看订单全额退款记录、退款状态和退款详情。</p>
        </div>
      </div>

      <div className="toolbar filter-bar">
        <form className="search-form" onSubmit={submitSearch}>
          <div className="search-box">
            <Search size={17} />
            <input
              placeholder="搜索退款号或订单号"
              value={keyword}
              onChange={(event) => setKeyword(event.target.value)}
            />
          </div>
          <select value={refundStatus} onChange={(event) => setRefundStatus(event.target.value)}>
            <option value="">全部退款状态</option>
            {refundStatusOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <button className="primary-button" type="submit">查询</button>
          <button className="secondary-button" type="button" onClick={resetFilters}>重置</button>
        </form>
        <button className="icon-button" title="刷新" type="button" onClick={() => loadRefunds()}>
          <RefreshCw size={17} />
        </button>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      {detail ? (
        <div className="record-form">
          <div className="form-heading">
            <h3>退款详情：{detail.refund_no}</h3>
            <button className="text-button" type="button" onClick={() => setDetail(null)}>关闭</button>
          </div>
          <div className="detail-grid">
            <span>订单号：{detail.order_no}</span>
            <span>支付流水号：{detail.payment_no}</span>
            <span>退款金额：{money(detail.refund_amount)}</span>
            <span>退款状态：<StatusBadge value={detail.refund_status} label={labelOf(detail.refund_status)} /></span>
            <span>申请人：{detail.requested_by}</span>
            <span>退款时间：{detail.refunded_at ? new Date(detail.refunded_at).toLocaleString() : '-'}</span>
          </div>
          <p>退款原因：{detail.refund_reason}</p>
          {detail.remark ? <p>备注：{detail.remark}</p> : null}
        </div>
      ) : null}

      <div className="table-panel">
        <table>
          <thead>
            <tr>
              <th>退款号</th>
              <th>订单号</th>
              <th>支付流水号</th>
              <th>退款金额</th>
              <th>退款状态</th>
              <th>申请人</th>
              <th>退款时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((refund) => (
              <tr key={refund.id}>
                <td>{refund.refund_no}</td>
                <td>{refund.order_no}</td>
                <td>{refund.payment_no}</td>
                <td>{money(refund.refund_amount)}</td>
                <td><StatusBadge value={refund.refund_status} label={labelOf(refund.refund_status)} /></td>
                <td>{refund.requested_by}</td>
                <td>{refund.refunded_at ? new Date(refund.refunded_at).toLocaleString() : '-'}</td>
                <td>
                  <button className="icon-button" title="查看详情" type="button" onClick={() => showDetail(refund.id)}>
                    <Eye size={16} />
                  </button>
                </td>
              </tr>
            ))}
            {data.items.length === 0 ? (
              <tr><td className="empty-cell" colSpan="8">暂无退款记录</td></tr>
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
