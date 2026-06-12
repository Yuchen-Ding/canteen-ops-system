const statusLabels = {
  ACTIVE: '启用',
  INACTIVE: '停用',
  ONLINE: '在线',
  OFFLINE: '离线',
  MAINTENANCE: '维护中',
  ERROR: '故障',
  PENDING: '待处理',
  PAID: '已支付',
  FAILED: '失败',
  REFUNDED: '已退款',
  CREATED: '已创建',
  COMPLETED: '已完成',
  CANCELLED: '已取消',
  SUCCESS: '成功',
};

const statusTones = {
  ACTIVE: 'success',
  ONLINE: 'success',
  PAID: 'success',
  COMPLETED: 'success',
  SUCCESS: 'success',
  INACTIVE: 'neutral',
  OFFLINE: 'neutral',
  REFUNDED: 'neutral',
  CANCELLED: 'neutral',
  PENDING: 'warning',
  CREATED: 'warning',
  MAINTENANCE: 'warning',
  ERROR: 'danger',
  FAILED: 'danger',
};

export function StatusBadge({ value, label }) {
  return (
    <span className={`status-badge ${statusTones[value] || 'neutral'}`}>
      {label || statusLabels[value] || value || '-'}
    </span>
  );
}
