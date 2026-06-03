# 监控计划

## 阶段 0

阶段 0 提供基础健康检查和 mock metrics：

- `/health`：服务是否启动。
- `/health/db`：数据库是否可连接。
- `/metrics`：返回基础状态指标。

## 后续增强方向

- 请求日志增加 request id。
- 业务异常增加结构化日志。
- POS 设备心跳状态进入监控指标。
- 订单支付失败、退款异常、补贴异常进入告警规则。
- 通过 `monitoring_adapter` 对接 Prometheus、云监控或日志平台。

## 指标规划

后续阶段可扩展：

- `backend_status`
- `database_status`
- `pos_online_count`
- `pos_offline_count`
- `order_created_total`
- `payment_failed_total`
- `refund_pending_total`
- `abnormal_transaction_total`
