# 架构说明

## 架构目标

本系统用于模拟企业餐厅运营管理的真实业务和部署形态。阶段 0 聚焦可部署工程骨架，确保后续业务模块可以按边界扩展，而不是堆叠成单体 CRUD。

## 逻辑分层

- Frontend：React 管理后台，所有页面展示中文，代码命名使用英文。
- Backend API：FastAPI 提供 REST API、健康检查、监控接口和业务服务入口。
- Modules：后续承载餐厅、档口、菜品、订单、支付、退款、补贴、报表等业务模块。
- Adapters：预留外部系统扩展点，第一版不接真实外部系统。
- Database：PostgreSQL 保存业务数据、系统版本和后续报表聚合数据。

## 阶段 1 后端模块结构

阶段 1 在 `backend/app/modules` 下按主数据资源拆分模块：

- `canteens`
- `stalls`
- `dishes`
- `meal_packages`
- `employees`
- `visitors`
- `devices`

每个模块包含 `model.py`、`schema.py`、`service.py`、`router.py`。公共 ORM Base、通用 CRUD 服务和标准路由工厂位于 `backend/app/common`。

## 阶段 1 主数据关系

- 一个 canteen 可以有多个 stalls。
- 一个 stall 属于一个 canteen。
- 一个 dish 属于一个 stall。
- 一个 meal_package 属于一个 stall。
- 一个 meal_package 可以通过 `meal_package_items` 包含多个 dishes。
- 一个 employee 可以绑定 `card_no`。
- 一个 visitor 作为访客消费对象。
- 一个 device 属于一个 canteen，也可以绑定到某个 stall。

## 适配器扩展点

后端已预留以下目录：

- `payment_adapter`：后续对接真实支付平台。
- `card_system_adapter`：后续对接真实刷卡或门禁卡系统。
- `employee_sync_adapter`：后续对接 HR 或企业组织系统。
- `finance_report_adapter`：后续对接财务报表或 ERP。
- `monitoring_adapter`：后续对接 Prometheus、日志平台或云监控。

## 部署拓扑

QA 环境建议部署在阿里云或华为云 Ubuntu 服务器中：

- `canteen_frontend_qa`：Nginx 托管 React 静态资源。
- `canteen_backend_qa`：FastAPI 服务。
- `canteen_postgres_qa`：PostgreSQL，仅容器网络内部访问。
- `canteen_network_qa`：项目专用 Docker network。
- `canteen_postgres_qa_data`：项目专用数据库 volume。

## 阶段 0 边界

阶段 0 不创建完整业务模型，不实现订单、支付、退款、补贴或报表逻辑。数据库仅包含系统版本和迁移记录基础表。

阶段 1 只实现主数据管理，不实现订单、支付、退款、补贴、报表或 AI。

## 阶段 2 交易关系

阶段 2 新增订单、订单明细和支付流水，交易数据与阶段 1 主数据建立引用关系：

- `orders.canteen_id` 引用 `canteens.id`。
- `orders.stall_id` 引用 `stalls.id`。
- `orders.device_id` 引用 `devices.id`。
- 员工消费时 `orders.employee_id` 引用 `employees.id`，`customer_type` 为 `EMPLOYEE`。
- 访客消费时 `orders.visitor_id` 可引用 `visitors.id`，也可以保存 `visitor_name_snapshot`。
- `order_items.order_id` 引用 `orders.id`。
- `order_items.dish_id` 可引用 `dishes.id`，同时保存菜品名称和价格快照。
- `payments.order_id` 引用 `orders.id`，阶段 2 一个订单只生成一条支付流水。

交易写入由 `backend/app/modules/pos` 负责，查询由 `orders` 和 `payments` 模块负责。阶段 2 仍然不接真实支付接口和真实刷卡硬件，支付结果由 mock 逻辑默认置为成功。

## 阶段 3 退款关系

- `refunds.order_id` 唯一引用 `orders.id`，限制一个订单只能生成一条全额退款记录。
- `refunds.payment_id` 唯一引用 `payments.id`。
- 退款服务使用订单行锁和支付流水行锁，降低并发重复退款风险。
- 退款成功后：
  - `orders.order_status = REFUNDED`
  - `orders.payment_status = REFUNDED`
  - `payments.payment_status = REFUNDED`
  - `refunds.refund_status = SUCCESS`

阶段 3 不调用 Payment Adapter 的真实渠道退款能力，只执行本地 mock 状态流转。

## 阶段 3 报表结构

`backend/app/modules/reports` 不拥有独立报表表，直接使用 PostgreSQL SQL 聚合：

- 订单指标来自 `orders`。
- 菜品排行来自 `order_items`。
- 退款金额来自状态为 `SUCCESS` 的 `refunds`。
- 餐厅和档口维度来自 `canteens`、`stalls`。

日报按 Asia/Shanghai 自然日统计，月报按自然月统计。

报表口径：

- `revenue`：周期内完成或已退款、且曾成功支付的订单应付金额。
- `refund_amount`：周期内成功退款记录的退款金额。
- `net_revenue = revenue - refund_amount`。

这种结构为后续 AI 日报和月报提供结构化数据，但阶段 3 不实现任何 AI 功能。

## 阶段 4 基础监控

`backend/app/modules/monitoring` 使用固定 SQLAlchemy 聚合查询主数据和状态，并复用 dashboard 报表服务获取今日业务指标。该模块不接入闸机、人流或真实设备心跳。

## 阶段 4 报表中心

前端将日报和月报合并为报表中心，支持日、月、年切换。后端年度报表按 Asia/Shanghai 自然年聚合，并返回十二个月的收入、退款和净收入趋势。

## 阶段 4 AI 助手

- `ai_chat_sessions` 保存会话。
- `ai_chat_messages` 保存 USER、ASSISTANT、SYSTEM 消息。
- `provider.py` 使用 `httpx` 调用 DeepSeek OpenAI-compatible chat completions API。
- API Key 只从 `DEEPSEEK_API_KEY` 环境变量读取，不进入前端、不写入仓库、不输出到日志。
- AI 上下文由 monitoring 和 reports 的固定服务函数生成。
- AI 没有 SQL 执行工具，不生成 SQL，不修改订单、支付、退款或主数据。
- 系统外问题由 system prompt 限制为提示“我主要基于当前食堂运营数据回答”。
