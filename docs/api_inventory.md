# API 清单

阶段 0 仅提供系统级接口，业务 API 从阶段 1 开始增加。

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/health` | 返回服务状态、版本、环境和时间戳 |
| GET | `/health/db` | 检查 PostgreSQL 连接状态 |
| GET | `/metrics` | 返回基础 mock metrics |
| GET | `/api/v1/system/info` | 返回系统名称、版本、环境和 AI provider |

## 阶段 1 主数据 API

每个主数据资源支持列表、详情、新增、编辑和状态更新。列表接口支持 `keyword`、`status`、`page`、`page_size`。

| Resource | Method | Path | 说明 |
| --- | --- | --- | --- |
| canteens | GET | `/api/v1/canteens` | 餐厅列表 |
| canteens | GET | `/api/v1/canteens/{id}` | 餐厅详情 |
| canteens | POST | `/api/v1/canteens` | 新增餐厅 |
| canteens | PUT | `/api/v1/canteens/{id}` | 编辑餐厅 |
| canteens | PATCH | `/api/v1/canteens/{id}/status` | 更新餐厅状态 |
| stalls | GET | `/api/v1/stalls` | 档口列表 |
| stalls | GET | `/api/v1/stalls/{id}` | 档口详情 |
| stalls | POST | `/api/v1/stalls` | 新增档口 |
| stalls | PUT | `/api/v1/stalls/{id}` | 编辑档口 |
| stalls | PATCH | `/api/v1/stalls/{id}/status` | 更新档口状态 |
| dishes | GET | `/api/v1/dishes` | 菜品列表 |
| dishes | GET | `/api/v1/dishes/{id}` | 菜品详情 |
| dishes | POST | `/api/v1/dishes` | 新增菜品 |
| dishes | PUT | `/api/v1/dishes/{id}` | 编辑菜品 |
| dishes | PATCH | `/api/v1/dishes/{id}/status` | 更新菜品状态 |
| meal_packages | GET | `/api/v1/meal-packages` | 套餐列表 |
| meal_packages | GET | `/api/v1/meal-packages/{id}` | 套餐详情 |
| meal_packages | POST | `/api/v1/meal-packages` | 新增套餐 |
| meal_packages | PUT | `/api/v1/meal-packages/{id}` | 编辑套餐 |
| meal_packages | PATCH | `/api/v1/meal-packages/{id}/status` | 更新套餐状态 |
| employees | GET | `/api/v1/employees` | 员工列表 |
| employees | GET | `/api/v1/employees/{id}` | 员工详情 |
| employees | POST | `/api/v1/employees` | 新增员工 |
| employees | PUT | `/api/v1/employees/{id}` | 编辑员工 |
| employees | PATCH | `/api/v1/employees/{id}/status` | 更新员工状态 |
| visitors | GET | `/api/v1/visitors` | 访客列表 |
| visitors | GET | `/api/v1/visitors/{id}` | 访客详情 |
| visitors | POST | `/api/v1/visitors` | 新增访客 |
| visitors | PUT | `/api/v1/visitors/{id}` | 编辑访客 |
| visitors | PATCH | `/api/v1/visitors/{id}/status` | 更新访客状态 |
| devices | GET | `/api/v1/devices` | POS 设备列表 |
| devices | GET | `/api/v1/devices/{id}` | POS 设备详情 |
| devices | POST | `/api/v1/devices` | 新增 POS 设备 |
| devices | PUT | `/api/v1/devices/{id}` | 编辑 POS 设备 |
| devices | PATCH | `/api/v1/devices/{id}/status` | 更新 POS 设备状态 |

## 阶段 2 交易 API

| Resource | Method | Path | 说明 |
| --- | --- | --- | --- |
| pos | POST | `/api/v1/pos/employee-card-payment` | 员工刷卡消费模拟 |
| pos | POST | `/api/v1/pos/visitor-qr-payment` | 访客扫码消费模拟 |
| orders | GET | `/api/v1/orders` | 订单列表，支持客户类型、支付状态、订单状态、餐厅、档口和时间过滤 |
| orders | GET | `/api/v1/orders/{id}` | 订单详情，返回订单、明细和支付记录 |
| payments | GET | `/api/v1/payments` | 支付流水列表，支持支付方式、支付状态和时间过滤 |

阶段 2 的支付均为 mock 支付，不调用真实支付宝、微信、银行卡或刷卡硬件接口。

## 命名约束

- API 路径统一使用英文。
- 枚举值统一使用英文。
- 数据库字段统一使用英文。
- 前端展示文本使用中文。
