# 企业餐厅运营管理系统

企业餐厅运营管理系统是一套面向企业餐厅行业最佳实践的原型系统。项目目标不是普通 CRUD，而是模拟真实企业餐厅在多地点运营、档口管理、消费交易、补贴计算、报表结算、设备监控、异常检测、AI 总结和环境部署中的核心能力。

阶段 0 已交付工程骨架、GitHub 友好结构和云服务器 QA 部署基线。阶段 1 已实现企业餐厅主数据管理，为后续交易闭环打基础。

## 技术架构

- Frontend: React + Vite + Nginx
- Backend: FastAPI + SQLAlchemy + asyncpg
- Database: PostgreSQL
- Deployment: Docker Compose
- AI: 默认 mock，后续预留 OpenAI、DeepSeek、Qwen provider

## 目录结构

```text
backend/                  FastAPI 后端工程
frontend/                 React 前端工程
database/                 PostgreSQL 初始化脚本
docs/                     中文业务、架构、部署和监控文档
scripts/                  本地和服务器运维脚本
docker/                   Docker 扩展配置目录
env/                      环境变量示例文件
.github/workflows/        GitHub Actions 基础 CI
```

## GitHub 使用方式

```bash
git init
git add .
git commit -m "stage 0 project baseline"
git branch -M main
git remote add origin git@github.com:<your-org-or-user>/<your-repo>.git
git push -u origin main
```

不要提交真实密钥。`env/.env.local`、`env/.env.qa`、`env/.env.prd` 已在 `.gitignore` 中排除。

## 本地最小启动方式

Mac 本地主要用于 Codex 开发和 Git 管理，不要求长期运行 Docker。本地只用于最小验证。

```bash
chmod +x scripts/*.sh
scripts/start-local.sh
```

访问地址：

- 前端：http://localhost:3100
- 后端健康检查：http://localhost:8100/health
- 数据库本地端口：`55432`

## 云服务器 QA 部署方式

服务器建议使用 Ubuntu 22.04 或 Ubuntu 24.04。

```bash
git clone git@github.com:<your-org-or-user>/<your-repo>.git
cd <your-repo>
cp env/.env.qa.example env/.env.qa
vim env/.env.qa
chmod +x scripts/*.sh
scripts/start-qa.sh
```

QA 环境默认端口：

- 前端：`3100`
- 后端：`8100`
- PostgreSQL：仅 Docker network 内部访问，不暴露公网端口

## 健康检查方式

```bash
scripts/smoke-test.sh
```

或指定服务器地址：

```bash
BASE_URL=http://<QA_SERVER_IP>:8100 scripts/smoke-test.sh
```

检查接口：

- `GET /health`
- `GET /health/db`
- `GET /api/v1/system/info`
- `GET /metrics`

## 阶段 1 已实现功能

阶段 1 只实现主数据管理，不实现订单、支付、退款、补贴、报表或 AI。

- 餐厅管理：维护餐厅编码、名称、城市、位置、状态。
- 档口管理：维护档口与餐厅归属关系。
- 菜品管理：维护档口菜品、品类、单价和可售状态。
- 套餐管理：维护套餐主体资料，数据库已预留套餐菜品明细表。
- 员工管理：维护员工编号、部门、员工类型和卡号。
- 访客管理：维护访客消费对象基础资料。
- POS 设备：维护设备编码、设备类型、所属餐厅、所属档口和设备状态。

主数据接口统一支持列表查询、详情查询、新增、编辑和状态更新。列表查询支持 `keyword`、`status`、`page`、`page_size`。

## 阶段 2 已实现功能

阶段 2 实现企业餐厅交易闭环基础，不接真实支付接口，不接真实刷卡硬件。

- 员工刷卡消费模拟：根据员工卡号、POS 设备、档口和菜品生成订单。
- 访客扫码消费模拟：支持已有访客或临时访客姓名，使用 mock 支付方式。
- 订单管理：查看订单列表和订单详情。
- 订单明细：保存菜品名称、单价和金额快照。
- 支付流水：记录 mock 支付结果，一个订单阶段 2 只生成一条支付记录。
- 支付状态流转：mock 支付默认成功，订单进入 `COMPLETED`，支付进入 `PAID`。

阶段 2 暂不实现退款审核、复杂结算、补贴规则、设备监控增强和 AI 总结。

## 环境说明

- local：本地最小验证，前端 `3100`，后端 `8100`，PostgreSQL 映射 `55432:5432`。
- qa：云服务器测试环境，前端 `3100`，后端 `8100`，PostgreSQL 不暴露到公网。
- prd：生产结构占位，不默认开放危险端口，不导入测试数据。

## 后续阶段路线

1. 阶段 1：多地点餐厅、档口、菜品、套餐、员工、访客、POS 设备主数据。
2. 阶段 2：员工刷卡消费、访客扫码支付、订单和支付状态闭环。
3. 阶段 3：退款、企业补贴规则、日报和月度结算报表。
4. 阶段 4：设备心跳、设备状态监控、异常交易检测。
5. 阶段 5：AI 日报和月报总结，默认 mock provider，预留外部模型接入。
6. 阶段 6：QA/PRD 运维增强、日志、监控、备份恢复和安全加固。

## 阶段 1 手工验收

启动环境后访问前端 `http://localhost:3100` 或 QA 服务器前端地址，依次进入餐厅管理、档口管理、菜品管理、套餐管理、员工管理、访客管理和 POS 设备。

每个页面验证列表加载、关键字搜索、状态筛选、新增、编辑、启用/停用。

## 阶段 2 手工验收

前端访问后依次验证：

- 员工刷卡消费：选择员工卡号、在线 POS 设备、档口、餐次和菜品，提交后返回订单号和已支付状态。
- 访客扫码消费：选择访客或输入临时访客姓名，选择支付方式和菜品，提交后生成订单和支付流水。
- 订单管理：可看到新订单，可查看订单详情和菜品明细。
- 支付流水：可看到新支付记录，可按支付方式和支付状态筛选。
